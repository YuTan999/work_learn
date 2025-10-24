# 主要改进点：
#
# 1.  结构优化：
# 添加了类初始化方法，将常量集中管理
# 引入了重试装饰器
# 改进了日志配置
# 2.  新功能：
# 文件存在性检查
# 升级状态监控
# 页面状态检查
# 带超时检查的等待函数
# 3.  错误处理：
# 改进了超时错误处理机制
# 添加了重试机制
# 完善了异常日志记录
# 4.  时间控制：
# 统一管理等待时间
# 更精确的周期控制
# 智能等待机制
# 5.  操作流程：
# 改进了登录验证
# 完善了升级确认流程
# 添加了状态检查


import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging
import functools


# 新增：改进日志配置
def setup_logging():
    log_filename = f'upgrade_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )


# 新增：重试装饰器
def retry_operation(max_retries=3, delay=5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"{func.__name__} 失败，尝试 {attempt + 1}/{max_retries}: {str(e)}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay)
            return None

        return wrapper

    return decorator


class Test123():
    def __init__(self):
        # 新增：配置常量
        self.CYCLE_TIME = 3600  # 60分钟
        self.WAIT_AFTER_V1 = 250  # V1上传后等待时间
        self.UPLOAD_WAIT_TIME = 20  # 上传等待时间
        self.UPGRADE_WAIT_TIME = 150  # 升级等待时间
        self.MAX_CYCLES = 15  # 最大循环次数
        self.FIRMWARE_PATHS = {
            'V1': r"E:\P-AVN-4_dev-r28640-p2-g3d75590c.tar",
            'V2': r"E:\P-AVN-4_dev-r28640-p1-g64e8e09d.tar"
        }

    def setup_method(self, method):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--ignore-certificate-errors')
        self.option.add_experimental_option("detach", True)
        self.driver = None
        self.init_driver()
        self.vars = {}
        self.wait = WebDriverWait(self.driver, 30)

    # 改进：初始化驱动
    @retry_operation()
    def init_driver(self):
        try:
            if self.driver:
                self.driver.quit()
            self.driver = webdriver.Chrome(options=self.option)
            self.driver.get("https://10.200.1.188/")
            return True
        except Exception as e:
            logging.error(f"初始化驱动失败: {str(e)}")
            raise

    # 新增：等待函数
    def wait_with_timeout(self, seconds, check_interval=5):
        end_time = time.time() + seconds
        while time.time() < end_time:
            try:
                self.driver.current_url
                time.sleep(check_interval)
            except:
                logging.error("等待过程中检测到页面异常")
                return False
        return True

    # 改进：元素等待
    def wait_for_element(self, by, value, timeout=30):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logging.error(f"等待元素超时: {value}")
            self.handle_timeout_error()
            return self.wait_for_element(by, value, timeout)

    # 改进：超时错误处理
    def handle_timeout_error(self):
        logging.info("正在处理超时错误...")
        try:
            self.driver.refresh()
            time.sleep(5)
            if "login" in self.driver.current_url.lower():
                self.login()
        except:
            self.init_driver()
            self.login()

    # 新增：检查页面状态
    def check_page_state(self):
        try:
            self.driver.current_url
            return True
        except:
            logging.error("页面状态异常，需要重新初始化")
            return False

    # 改进：登录函数
    @retry_operation()
    def login(self):
        try:
            time.sleep(2)
            username = self.wait_for_element(By.NAME, "username")
            username.send_keys("admin")
            password = self.wait_for_element(By.NAME, "password")
            password.send_keys("proav101")
            password.send_keys(Keys.ENTER)
            self.wait_for_element(By.LINK_TEXT, "Device List")  # 验证登录成功
        except Exception as e:
            logging.error(f"登录失败: {str(e)}")
            raise

    # 改进：上传循环
    def perform_upload_cycle(self, cycle_count):
        try:
            logging.info(f"开始执行第 {cycle_count} 个循环")
            self.cycle_start_time = time.time()

            button = self.wait_for_element(By.LINK_TEXT, "Device List")
            button.click()
            time.sleep(5)

            self.turn_to_settings()

            # 上传V1
            logging.info(f"循环 {cycle_count}: 准备上传 V1")
            self.upload_file(self.FIRMWARE_PATHS['V1'])
            self.wait_with_timeout(self.WAIT_AFTER_V1)

            self.turn_to_settings()

            # 上传V2
            logging.info(f"循环 {cycle_count}: 准备上传 V2")
            self.upload_file(self.FIRMWARE_PATHS['V2'])

            # 等待完成循环
            elapsed_time = time.time() - self.cycle_start_time
            remaining_time = self.CYCLE_TIME - elapsed_time
            if remaining_time > 0:
                logging.info(f"等待剩余时间: {remaining_time:.0f} 秒")
                self.wait_with_timeout(remaining_time)

        except Exception as e:
            logging.error(f"循环执行过程中发生错误: {str(e)}")
            self.handle_timeout_error()

    # 新增：文件检查
    def verify_file_exists(self, file_path):
        if not os.path.exists(file_path):
            logging.error(f"文件不存在: {file_path}")
            raise FileNotFoundError(f"升级文件不存在: {file_path}")
        file_size = os.path.getsize(file_path)
        logging.info(f"文件大小: {file_size / 1024 / 1024:.2f}MB")

    # 改进：设置页面导航
    def turn_to_settings(self):
        root_checkbox = self.wait_for_element(By.XPATH,
                                              "//*[@id='root']/div/main/div[3]/table/thead/tr/th[1]/span/input")
        self.driver.execute_script("arguments[0].click();", root_checkbox)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", root_checkbox)
        time.sleep(1)
        test_checkbox = self.wait_for_element(By.XPATH,
                                              "//*[@id='root']/div/main/div[3]/table/tbody/tr[1]/td/table/thead/tr/th[1]/span/input")
        self.driver.execute_script("arguments[0].click();", test_checkbox)

        second_element = self.wait_for_element(By.CSS_SELECTOR, ".css-o2hjg:nth-child(2)")
        second_element.click()

    def back_to_list(self):
        back_button = self.wait_for_element(By.CSS_SELECTOR, ".css-1yjo05o > .MuiButton-outlined")
        back_button.click()

    # 新增：升级状态检查
    def check_upgrade_status(self):
        try:
            progress = self.wait_for_element(By.CSS_SELECTOR, ".progress-indicator", timeout=5)
            if progress:
                return "upgrading"
            success = self.wait_for_element(By.CSS_SELECTOR, ".success-indicator", timeout=5)
            if success:
                return "success"
            return "unknown"
        except TimeoutException:
            return "no_progress"

    # 改进：文件上传
    def upload_file(self, file_path):
        try:
            self.verify_file_exists(file_path)

            error_icon = self.wait_for_element(By.CSS_SELECTOR, ".MuiSvgIcon-colorError > path")
            error_icon.click()

            error_button = self.wait_for_element(By.CSS_SELECTOR, ".MuiButton-containedError")
            error_button.click()
            time.sleep(3)

            file_input = self.wait_for_element(By.XPATH, "// *[ @ id = 'fwFile-file']")
            file_input.send_keys(file_path)
            logging.info(f"文件上传开始: {file_path}")

            time.sleep(self.UPLOAD_WAIT_TIME)

            update_button = self.wait_for_element(By.CSS_SELECTOR, "span > .MuiButton-root")
            update_button.click()
            update_check = self.wait_for_element(By.CSS_SELECTOR, ".MuiDialogActions-root > .MuiButton-contained")
            update_check.click()
            logging.info("升级中...")

            time.sleep(self.UPGRADE_WAIT_TIME)

            status = self.check_upgrade_status()
            logging.info(f"升级状态: {status}")

            self.back_to_list()

        except Exception as e:
            logging.error(f"升级过程中发生错误: {str(e)}")
            self.handle_timeout_error()

    def est_123(self):
        self.login()
        cycle_count = 1
        while cycle_count <= self.MAX_CYCLES:
            try:
                self.cycle_start_time = time.time()
                self.perform_upload_cycle(cycle_count)
                cycle_count += 1
            except Exception as e:
                logging.error(f"主循环中发生错误: {str(e)}")
                self.handle_timeout_error()

    def teardown_method(self, method):
        if self.driver:
            self.driver.quit()


def main():
    setup_logging()
    while True:
        try:
            test = Test123()
            test.setup_method(None)
            test.est_123()
            test.teardown_method(None)
            break
        except Exception as e:
            logging.error(f"主程序发生错误: {str(e)}")
            time.sleep(60)


if __name__ == "__main__":
    main()