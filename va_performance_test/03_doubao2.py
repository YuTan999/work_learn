import threading
import time
import random
import requests
import logging
import csv
from datetime import datetime
from pathlib import Path

# 配置日志输出格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 禁用不安全请求警告
requests.packages.urllib3.disable_warnings()

# 配置参数
LOGIN_URL = "http://10.200.1.191/api/v1/auth/login"
RESOURCE_URL = "http://10.200.1.191/api/v1/resource/resources"
USERNAME = "admin"
PASSWORD = "proav101"
THREAD_COUNT = 367  # 并发线程数，对应12个用户
REQUESTS_PER_THREAD = 10  # 每个线程发送的请求数
CSV_FILENAME = f"request_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"  # CSV日志文件名

# 存储测试结果
results = {
    "success": 0,
    "failed": 0,
    "total_time": 0,
    "response_times": [],
    "request_count": 0,  # 全局请求序号
    "errors": []  # 错误信息记录
}

# 线程锁，用于安全地更新结果和写入CSV
lock = threading.Lock()


def init_csv():
    """初始化CSV文件并写入表头"""
    with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "请求序号",
            "时间戳",
            "Cookie",
            "响应时间(毫秒)",
            "状态",
            "错误信息"
        ])
    logger.info(f"已初始化CSV日志文件: {CSV_FILENAME}")


def write_to_csv(request_num, timestamp, cookie_str, response_time, status, error_msg=""):
    """将请求详情写入CSV文件"""
    with lock:  # 确保多线程安全写入
        with open(CSV_FILENAME, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                request_num,
                timestamp,
                cookie_str,
                f"{response_time:.3f}",
                status,
                error_msg
            ])


def login():
    """执行登录并返回获取到的cookie"""
    try:
        payload = {
            "user": USERNAME,
            "password": PASSWORD
        }
        response = requests.post(LOGIN_URL, json=payload, verify=False)
        response.raise_for_status()

        login_data = response.json()
        if login_data.get("success"):
            cookie_key = login_data["cookie"]["key"]
            cookie_value = login_data["cookie"]["value"]
            cookie = {cookie_key: cookie_value}
            logger.info(f"登录成功，获取到cookie: {cookie}")
            return cookie
        else:
            error_msg = f"登录失败: {login_data.get('message', '未知错误')}"
            logger.error(error_msg)
            return None
    except Exception as e:
        error_msg = f"登录过程出错: {str(e)}"
        logger.error(error_msg)
        return None


def test_resource_endpoint(cookie):
    """测试资源接口，记录请求序号、cookie和响应时间并写入CSV"""
    # 获取全局请求序号
    with lock:
        results["request_count"] += 1
        request_num = results["request_count"]  # 当前请求序号

    # 格式化cookie为字符串
    cookie_str = "; ".join([f"{k}={v}" for k, v in cookie.items()]) if cookie else "无有效cookie"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # 保留毫秒的时间戳
    status = "失败"
    error_msg = ""

    try:
        start_time = time.time()
        response = requests.get(RESOURCE_URL, cookies=cookie, verify=False)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # 转换为毫秒

        # 记录当前请求详情到日志
        logger.info(f"请求 #{request_num} - Cookie: {cookie_str} - 响应时间: {response_time:.3f}毫秒")

        with lock:
            results["response_times"].append(response_time)

            if response.status_code == 200:
                results["success"] += 1
                status = "成功"
            else:
                results["failed"] += 1
                error_msg = f"状态码: {response.status_code}"
                results["errors"].append({
                    "time": timestamp,
                    "response_time": response_time / 1000,  # 转换为秒
                    "error": error_msg
                })
                logger.warning(f"请求 #{request_num} 失败，{error_msg}")

        # 写入CSV
        write_to_csv(request_num, timestamp, cookie_str, response_time, status, error_msg)

    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        error_msg = str(e)
        with lock:
            results["failed"] += 1
            results["errors"].append({
                "time": timestamp,
                "response_time": response_time / 1000,  # 转换为秒
                "error": error_msg
            })
        logger.error(f"请求 #{request_num} - Cookie: {cookie_str} 出错: {error_msg}")
        # 写入CSV
        write_to_csv(request_num, timestamp, cookie_str, response_time, status, error_msg)


def thread_task():
    """线程任务：每个线程使用独立cookie发送请求"""
    # 每个线程独立登录，获取自己的cookie
    cookie = login()
    if not cookie:
        logger.error(f"线程 {threading.current_thread().name} 登录失败，无法执行任务")
        return

    # 发送指定次数的请求
    for _ in range(REQUESTS_PER_THREAD):
        # 随机延迟模拟用户操作间隔
        time.sleep(random.uniform(0.1, 0.2))
        test_resource_endpoint(cookie)


def run_stress_test():
    """运行多用户并发压力测试"""
    # 初始化CSV文件
    init_csv()

    logger.info("===== 开始多用户并发测试 =====")
    logger.info(f"并发用户数: {THREAD_COUNT}")
    logger.info(f"每个用户请求数: {REQUESTS_PER_THREAD}")
    logger.info(f"总请求数: {THREAD_COUNT * REQUESTS_PER_THREAD}")
    logger.info(f"请求详情将记录到: {CSV_FILENAME}")

    start_time = time.time()

    # 创建并启动线程
    threads = []
    for i in range(THREAD_COUNT):
        thread = threading.Thread(target=thread_task, name=f"User-{i + 1}")
        threads.append(thread)
        thread.start()
        logger.info(f"启动用户线程 {i + 1}/{THREAD_COUNT}")

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    end_time = time.time()
    results["total_time"] = end_time - start_time

    # 计算统计数据
    total = results["success"] + results["failed"]
    batch_avg_time = sum(results["response_times"]) / len(results["response_times"]) / 1000 if results[
        "response_times"] else 0
    batch_min_time = min(results["response_times"]) / 1000 if results["response_times"] else 0
    batch_max_time = max(results["response_times"]) / 1000 if results["response_times"] else 0

    # 输出测试结果日志
    logger.info("\n========== 请求统计 ==========")
    logger.info(f"总请求次数: {total}")
    logger.info(f"成功次数: {results['success']} ({(results['success'] / total * 100 if total else 0):.2f}%)")
    logger.info(f"失败次数: {results['failed']} ({(results['failed'] / total * 100 if total else 0):.2f}%)")

    logger.info("\n=== 当前批次统计 ===")
    logger.info(f"平均响应时间: {batch_avg_time:.3f}秒")
    logger.info(f"最小响应时间: {batch_min_time:.3f}秒")
    logger.info(f"最大响应时间: {batch_max_time:.3f}秒")

    logger.info("\n=== 累计统计 ===")
    logger.info(f"平均响应时间: {batch_avg_time:.3f}秒")
    logger.info(f"最小响应时间: {batch_min_time:.3f}秒")
    logger.info(f"最大响应时间: {batch_max_time:.3f}秒")

    # 关键指标强调
    logger.info(f"★ 总计失败次数: {results['failed']}")
    logger.info(f"★ 历史最大响应时间: {batch_max_time:.3f}秒")

    if results['errors']:
        logger.info("\n========== 最近5个错误 ==========")
        for error in results['errors'][-5:]:
            logger.info(f"[{error['time']}] 响应时间: {error['response_time']:.3f}秒, 错误: {error['error']}")

    logger.info(f"\n总耗时: {results['total_time']:.2f}秒")
    logger.info(f"每秒请求数(TPS): {total / results['total_time']:.2f}")
    logger.info("===== 测试结束 =====")
    logger.info(f"完整请求日志已保存至: {CSV_FILENAME}")


if __name__ == "__main__":
    run_stress_test()
