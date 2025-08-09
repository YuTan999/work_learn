import threading
import time
import json
from datetime import datetime
import random
import requests

# 禁用不安全请求警告
requests.packages.urllib3.disable_warnings()

# 配置参数
LOGIN_URL = "http://10.200.1.191/api/v1/auth/login"
RESOURCE_URL = "http://10.200.1.191/api/v1/resource/resources"
USERNAME = "admin"
PASSWORD = "proav101"
THREAD_COUNT = 10  # 并发线程数
REQUESTS_PER_THREAD = 100  # 每个线程发送的请求数

# 存储测试结果
results = {
    "success": 0,
    "failed": 0,
    "total_time": 0,
    "response_times": []
}

# 线程锁，用于安全地更新结果
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
            print(f"登录失败: {login_data.get('message', '未知错误')}")
            return None
    except Exception as e:
        print(f"登录过程出错: {str(e)}")
        return None


def test_resource_endpoint(cookie):
    """测试资源接口"""
    try:
        start_time = time.time()
        response = requests.get(RESOURCE_URL, cookies=cookie, timeout=10, verify=False)
        end_time = time.time()
        print(response.json())
        response_time = (end_time - start_time) * 1000  # 转换为毫秒

        with lock:
            results["response_times"].append(response_time)

            if response.status_code == 200:
                results["success"] += 1
            else:
                results["failed"] += 1
                print(f"请求失败，状态码: {response.status_code}")

    except Exception as e:
        with lock:
            results["failed"] += 1
        print(f"请求过程出错: {str(e)}")


def thread_task(cookie):
    """线程执行的任务"""
    for _ in range(REQUESTS_PER_THREAD):
        # 随机添加一些延迟，模拟真实用户行为
        time.sleep(random.uniform(0.1, 0.5))
        test_resource_endpoint(cookie)


def run_stress_test():
    """运行压力测试"""
    # 先执行登录
    print("正在执行登录...")
    cookie = login()
    print(cookie)
    if not cookie:
        print("登录失败，无法进行压力测试")
        return

    print(f"登录成功，开始压力测试...")
    print(f"并发线程数: {THREAD_COUNT}")
    print(f"每个线程请求数: {REQUESTS_PER_THREAD}")
    print(f"总请求数: {THREAD_COUNT * REQUESTS_PER_THREAD}")

    start_time = time.time()

    # 创建并启动线程
    threads = []
    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=thread_task, args=(cookie,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    end_time = time.time()
    results["total_time"] = end_time - start_time

    # 输出测试结果
    print("\n===== 压测结果 =====")
    print(f"总请求数: {THREAD_COUNT * REQUESTS_PER_THREAD}")
    print(f"成功请求数: {results['success']}")
    print(f"失败请求数: {results['failed']}")
    print(f"成功率: {results['success'] / (results['success'] + results['failed']) * 100:.2f}%")
    print(f"总耗时: {results['total_time']:.2f}秒")
    print(f"平均请求时间: {sum(results['response_times']) / len(results['response_times']):.2f}毫秒")
    print(f"最大请求时间: {max(results['response_times']):.2f}毫秒")
    print(f"最小请求时间: {min(results['response_times']):.2f}毫秒")
    print(f"每秒请求数(TPS): {(results['success'] + results['failed']) / results['total_time']:.2f}")


if __name__ == "__main__":
    run_stress_test()
