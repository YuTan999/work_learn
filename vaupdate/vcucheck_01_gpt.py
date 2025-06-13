import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import logging

# 配置日志
logging.basicConfig(
    filename='test_results1.log',
    level=logging.INFO,
    format='%(message)s'
)


def login(driver, url):
    """登录方法"""
    driver.get(url)
    try:
        time.sleep(2)
        username = driver.find_element(By.NAME, "username")
        username.send_keys("admin")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("proav101")
        password.send_keys(Keys.ENTER)
    except Exception as e:
        logging.error(f"登录失败: {str(e)}")
    pass


def check_status(driver, ip):
    """检查状态并记录结果"""
    try:
        # 等待元素可见
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//div[@id='root']/div/main/div/div[2]/div[2]/div[3]/div[2]/div/div/div[2]/div/div/div/div/div/div[1]/div[1]/*[name()='svg']"))
        )
        time.sleep(1)
        # 获取元素的class属性
        class_attr = element.get_attribute("class")

        # 判断结果
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "MuiSvgIcon-colorPrimary" in class_attr:
            result = "PASS"
        elif "MuiSvgIcon-colorError" in class_attr:
            result = "FAIL"
        else:
            result = "UNKNOWN-"+class_attr

        # 记录日志
        logging.info(f"[{current_time}] {ip} {result}")
        return result

    except Exception as e:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"[{current_time}] {ip} ERROR: {str(e)}")
        return "ERROR"


def main():
    # IP地址列表
    ip_list = [
        # TODO: 添加需要测试的IP地址
        "http://10.200.1.31",
        "http://10.200.1.32",
        "http://10.200.1.33",
        "http://10.200.1.34",
        "http://10.200.1.35",
        "http://10.200.1.36",
        "http://10.200.1.37",
        "http://10.200.1.39",
        "http://10.200.1.40",
        "http://10.200.1.41",
        "http://10.200.1.42",
        "http://10.200.1.47",
        "http://10.200.1.48",
        "http://10.200.1.50",
        "http://10.200.1.53",
        "http://10.200.1.54",
        "http://10.200.1.55"
    ]

    # 初始化计数器
    pass_count = 0
    fail_count = 0
    error_count = 0
    chrome_driver_path = r'E:\jetbrain software\python\chromedriver-win64\chromedriver.exe'
    service = Service(chrome_driver_path)
    # 初始化WebDriver
    driver = webdriver.Chrome(service=service)
    # 初始化webdriver
    # driver = webdriver.Chrome()  # 或使用其他浏览器驱动

    try:
        for ip in ip_list:
            # 登录
            login(driver, ip)

            # 检查状态
            result = check_status(driver, ip)

            # 统计结果
            if result == "PASS":
                pass_count += 1
            elif result == "FAIL":
                fail_count += 1
            else:
                error_count += 1

    finally:
        driver.quit()

    # 记录总结果
    logging.info("\n=== Summary ===")
    logging.info(f"Total tests: {len(ip_list)}")
    logging.info(f"PASS: {pass_count}")
    logging.info(f"FAIL: {fail_count}")
    logging.info(f"ERROR: {error_count}")


if __name__ == "__main__":
    main()