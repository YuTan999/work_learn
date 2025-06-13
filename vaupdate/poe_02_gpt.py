# coding=gbk
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


def setup_logging():
    log_filename = f'poe_upgrade_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


class Test123():
    def __init__(self):
        # self.CYCLE_TIME = 200  # 30分钟
        self.CYCLE_TIME = 1420  # 30分钟
        self.OPERATION_WAIT = 5  # 基础操作等待时间
        self.APPLY_WAIT = 30  # Apply等待时间
        self.MAX_CYCLES = 150  # 最大循环次数
        self.URL = "http://10.200.0.74/"
        self.driver = None
        self.cycle_start_time = None

    def setup_method(self, method):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--ignore-certificate-errors')
        # self.option.binary_location = "E:\jetbrain software\python\chromedriver-win64\chromedriver.exe"
        self.init_driver()
        self.vars = {}
        self.wait = WebDriverWait(self.driver, 30)

    def init_driver(self):
        try:
            if self.driver:
                self.driver.quit()
            chrome_driver_path = r'E:\jetbrain software\python\chromedriver-win64\chromedriver.exe'
            service = Service(chrome_driver_path)
            self.driver = webdriver.Chrome(options=self.option,service=service)
            self.driver.get(self.URL)
            logging.info(f"成功初始化驱动并访问 {self.URL}")
            return True
        except Exception as e:
            logging.error(f"初始化驱动失败: {str(e)}")
            raise

    def wait_for_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logging.error(f"等待元素超时: {value}")
            self.handle_timeout_error()
            return self.wait_for_element(by, value, timeout)

    def handle_timeout_error(self):
        logging.info("正在处理超时错误...")
        time.sleep(2)
        # try:
        #     self.driver.refresh()
        #     time.sleep(5)
        #     if "login" in self.driver.current_url.lower():
        #         self.init_driver()
        #         self.login()
        # except:
        #     self.init_driver()
        #     self.login()
        # elapsed_time = time.time() - self.cycle_start_time
        # remaining_time = self.CYCLE_TIME - elapsed_time  # 40分钟 = 2400秒
        # if remaining_time > 0:
        #     logging.info(f"等待剩余时间: {remaining_time:.0f} 秒")
        #     time.sleep(remaining_time)
        self.init_driver()
        self.est_123()

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

    def login(self):
        try:
            time.sleep(self.OPERATION_WAIT)
            username = self.wait_for_element(By.XPATH,
                                             "//div[@id='app']/div/div/div/div[2]/div/form/div/div/fieldset/div/div/input")
            username.send_keys("admin")

            password = self.wait_for_element(By.XPATH, "//input[@type='password']")
            password.send_keys("sencore123")
            password.send_keys(Keys.ENTER)

            time.sleep(self.OPERATION_WAIT)
            logging.info("登录成功")

            # 点击菜单第6项
            menu_item = self.wait_for_element(By.CSS_SELECTOR, ".is-active .el-menu-item:nth-child(6)")
            menu_item.click()
            time.sleep(self.OPERATION_WAIT)

        except Exception as e:
            logging.error(f"登录失败: {str(e)}")
            self.handle_timeout_error()

    def enter_settings(self):
        """进入设置页面"""
        try:
            logging.info("进入设置页面...")

            # 进入设置
            settings_button = self.wait_for_element(By.CSS_SELECTOR, ".el-button--text:nth-child(2) > span")
            settings_button.click()
            time.sleep(self.OPERATION_WAIT)
            logging.info("成功进入设置页面")
        except Exception as e:
            logging.error(f"进入设置页面失败: {str(e)}")
            self.handle_timeout_error()

    def select_device(self):
        """选中设备"""
        try:
            checkbox = self.wait_for_element(By.CSS_SELECTOR, ".mt20 .el-checkbox__inner")
            checkbox.click()
            time.sleep(self.OPERATION_WAIT)
            # 少选一台
            # port_23 = self.wait_for_element(By.CSS_SELECTOR,
            #                                 ".net-work-row:nth-child(1) > .net-work-port:nth-child(12) .lan-content:nth-child(2) .lan-font")
            # port_23.click()
            time.sleep(self.OPERATION_WAIT)
            logging.info("成功选中设备")
        except Exception as e:
            logging.error(f"选中设备失败: {str(e)}")
            self.handle_timeout_error()

    def toggle_switch(self):
        """点击开关"""
        try:
            switch = self.wait_for_element(By.CSS_SELECTOR, ".el-switch__core")
            switch.click()
            time.sleep(self.OPERATION_WAIT)
            logging.info("成功点击开关")
        except Exception as e:
            logging.error(f"点击开关失败: {str(e)}")
            self.handle_timeout_error()

    def click_apply(self):
        """点击apply按钮"""
        try:
            apply_button = self.wait_for_element(By.CSS_SELECTOR,
                                                 ".el-dialog__footer:nth-child(3) .el-button--primary")
            apply_button.click()
            time.sleep(self.APPLY_WAIT)
            logging.info("成功点击Apply按钮")
        except Exception as e:
            logging.error(f"点击Apply按钮失败: {str(e)}")
            self.handle_timeout_error()

    def perform_settings_operations(self):
        """执行完整的设置操作流程"""
        try:
            logging.info("开始第一轮设置操作...")
            # 第一轮操作
            self.enter_settings()
            self.select_device()
            self.toggle_switch()
            self.click_apply()

            self.driver.refresh()

            logging.info("开始第二轮设置操作...")
            # 第二轮操作
            self.enter_settings()
            self.select_device()
            self.click_apply()

            logging.info("设置操作完成")
        except Exception as e:
            logging.error(f"设置操作失败: {str(e)}")
            self.handle_timeout_error()

    def perform_cycle(self, cycle_count):
        try:
            logging.info(f"开始执行第 {cycle_count} 个循环")
            self.cycle_start_time = time.time()

            self.perform_settings_operations()

            # 计算并等待剩余时间
            elapsed_time = time.time() - self.cycle_start_time
            remaining_time = self.CYCLE_TIME - elapsed_time
            if remaining_time > 0:
                logging.info(f"等待剩余时间: {remaining_time:.0f} 秒")
                # self.wait_with_timeout(remaining_time)
                time.sleep(remaining_time)
            self.init_driver()


        except Exception as e:
            logging.error(f"循环执行过程中发生错误: {str(e)}")
            self.handle_timeout_error()

    def est_123(self):
        self.login()
        cycle_count = 1
        while cycle_count <= self.MAX_CYCLES:
            try:
                self.perform_cycle(cycle_count)
                cycle_count += 1
            except Exception as e:
                logging.error(f"主循环中发生错误: {str(e)}")
                self.handle_timeout_error()

    def teardown_method(self, method):
        if self.driver:
            self.driver.quit()
            logging.info("已关闭浏览器驱动")


def main():
    setup_logging()
    logging.info("程序启动")
    while True:
        try:
            test = Test123()
            test.setup_method(None)
            test.est_123()
            test.teardown_method(None)
            logging.info("程序正常完成")
            break
        except Exception as e:
            logging.error(f"主程序发生错误: {str(e)}")
            time.sleep(60)


if __name__ == "__main__":
    main()
