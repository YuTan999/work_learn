import threading
import time
import json
import random
import requests
import logging
from datetime import datetime

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
THREAD_COUNT = 10  # 并发线程数
REQUESTS_PER_THREAD = 100  # 每个线程发送的请求数
COOKIE_COUNT = 12  # 预获取的cookie数量

# 存储测试结果
results = {
    "success": 0,
    "failed": 0,
    "total_time": 0,
    "response_times": [],
    "errors": [],  # 错误信息
    "request_count": 0  # 用于记录全局请求序号
}

# 存储获取到的cookies
cookies = []

# 线程锁，用于安全地更新结果和获取cookie
lock = threading.Lock()


def login():
    """执行登录并返回获取到的cookie"""
    try:
        payload = {
            "user": USERNAME,
            "password": PASSWORD
        }
        response = requests.post(LOGIN_URL, json=payload, timeout=10, verify=False)
        response.raise_for_status()

        login_data = response.json()
        if login_data.get("success"):
            cookie_key = login_data["cookie"]["key"]
            cookie_value = login_data["cookie"]["value"]
            return {cookie_key: cookie_value}
        else:
            error_msg = f"登录失败: {login_data.get('message', '未知错误')}"
            logger.error(error_msg)
            return None
    except Exception as e:
        error_msg = f"登录过程出错: {str(e)}"
        logger.error(error_msg)
        return None


def get_next_cookie():
    """循环获取下一个可用的cookie"""
    with lock:
        if not cookies:
            return None
        # 取出第一个cookie并移到末尾，实现轮询效果
        cookie = cookies.pop(0)
        cookies.append(cookie)
        return cookie


def test_resource_endpoint():
    """测试资源接口，使用轮询的cookie"""
    with lock:
        results["request_count"] += 1
        request_num = results["request_count"]  # 当前请求序号
# 获取一个cookie
    cookie = get_next_cookie()
    cookie_str = "; ".join([f"{k}={v}" for k, v in cookie.items()]) if cookie else "无有效cookie"
    if not cookie:
        error_msg = "没有可用的cookie，无法发送请求"
        logger.error(error_msg)
        with lock:
            results["failed"] += 1
            results["errors"].append({
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "response_time": 0,
                "error": error_msg
            })
        return

    try:
        start_time = time.time()
        response = requests.get(RESOURCE_URL, cookies=cookie, timeout=10, verify=False)
        end_time = time.time()
        response_time = end_time - start_time  # 保留为秒用于统计

        # 打印响应内容（根据需要保留或删除）
        # logger.debug(f"响应内容: {response.json()}")
        print(f"请求 #{request_num} - Cookie: {cookie_str} - 响应时间: {response_time:.3f}毫秒")

        with lock:
            results["response_times"].append(response_time)

            if response.status_code == 200:
                results["success"] += 1
            else:
                results["failed"] += 1
                error_msg = f"请求失败，状态码: {response.status_code}"
                results["errors"].append({
                    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "response_time": response_time,
                    "error": error_msg
                })
                logger.warning(error_msg)

    except Exception as e:
        response_time = time.time() - start_time
        error_msg = f"请求过程出错: {str(e)}"
        with lock:
            results["failed"] += 1
            results["errors"].append({
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "response_time": response_time,
                "error": error_msg
            })
        logger.error(error_msg)


def thread_task():
    """线程执行的任务"""
    for _ in range(REQUESTS_PER_THREAD):
        # 随机添加一些延迟，模拟真实用户行为
        time.sleep(random.uniform(0.1, 0.5))
        test_resource_endpoint()


def run_stress_test():
    """运行压力测试"""
    # 先执行多次登录获取多个cookie
    logger.info(f"正在获取{COOKIE_COUNT}个登录cookie...")
    global cookies
    for i in range(COOKIE_COUNT):
        logger.info(f"获取第{i + 1}个cookie...")
        cookie = login()
        if cookie:
            cookies.append(cookie)
            logger.info(f"获取第{i + 1}个cookie...{cookie}")

        else:
            logger.warning(f"获取第{i + 1}个cookie失败")

    if not cookies:
        logger.error("未能获取到任何有效cookie，无法进行压力测试")
        return

    logger.info(f"成功获取到{len(cookies)}个cookie，开始压力测试...")
    logger.info(f"并发线程数: {THREAD_COUNT}")
    logger.info(f"每个线程请求数: {REQUESTS_PER_THREAD}")
    logger.info(f"总请求数: {THREAD_COUNT * REQUESTS_PER_THREAD}")

    start_time = time.time()

    # 创建并启动线程
    threads = []
    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=thread_task)
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    end_time = time.time()
    results["total_time"] = end_time - start_time

    # 计算统计数据
    total = results["success"] + results["failed"]
    batch_avg_time = sum(results["response_times"]) / len(results["response_times"]) if results["response_times"] else 0
    batch_min_time = min(results["response_times"]) if results["response_times"] else 0
    batch_max_time = max(results["response_times"]) if results["response_times"] else 0

    # 输出测试结果日志
    logger.info("\n========== 请求统计 ==========")
    logger.info(f"总请求次数: {total}")
    logger.info(f"成功次数: {results['success']} ({(results['success'] / total * 100 if total else 0):.2f}%)")
    logger.info(f"失败次数: {results['failed']} ({(results['failed'] / total * 100 if total else 0):.2f}%)")

    logger.info("\n=== 当前批次统计 ===")
    logger.info(f"平均响应时间: {batch_avg_time:.3f}秒")
    logger.info(f"最小响应时间: {batch_min_time:.3f}秒")
    logger.info(f"最大响应时间: {batch_max_time:.3f}秒")

    # 新增的两条专用日志
    logger.info(f"★ 总计失败次数: {results['failed']}")
    logger.info(f"★ 历史最大响应时间: {batch_max_time:.3f}秒")

    if results['errors']:
        logger.info("\n========== 最近5个错误 ==========")
        for error in results['errors'][-5:]:
            logger.info(f"[{error['time']}] 响应时间: {error['response_time']:.3f}秒, 错误: {error['error']}")

    logger.info(f"\n总耗时: {results['total_time']:.2f}秒")
    logger.info(f"每秒请求数(TPS): {total / results['total_time']:.2f}")


if __name__ == "__main__":
    run_stress_test()
