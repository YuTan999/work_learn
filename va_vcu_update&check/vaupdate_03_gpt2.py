# gpt优化、封装的代码：
# 四十分钟为一个循环周期，第一分钟上传V1，等待七分钟后上传V2，直到第四十一分钟再进入下一个循环。请帮我修改代码，并注意不会因为超时错误而停止执行
# 添加了完整的错误处理机制
# 实现了精确的时间控制（40分钟为一个周期）
# 添加了详细的日志记录
# 增加了自动重试机制
# 优化了等待时间的控制
# 添加了防止浏览器自动关闭的选项
# 增加了网页元素等待时间
# 分离了上传文件的逻辑为独立函数
# 实现了在发生错误时的自动恢复机制
#
# 代码的主要特点：
# 每个循环周期为40分钟
# 循环开始时上传V1
# 等待7分钟后上传V2
# 自动计算剩余等待时间以保持40分钟的周期
# 所有操作都有错误处理和重试机制
# 详细的日志记录，方便追踪问题

# 我调整了重试的细节等：
# 1.  时间控制更合理
# 周期从40分钟(2400秒)改为60分钟(3600秒)
# V1上传后等待时间从420秒改为250秒
# 更合理的文件上传等待时间(从30秒改为20秒)
# 2.  功能拆分更细致
# 新增turn_to_settings()方法
# 新增back_to_list()方法
# 更清晰的功能模块划分
# 3.  操作流程优化
# 改进了checkbox选择逻辑（双击root checkbox）
# 新增确认升级步骤
# 更精确的元素定位xpath
# 4.  代码结构改进
# 设备选择逻辑独立封装
# 页面导航逻辑独立封装
# 减少了代码重复
# 5.  错误处理改进
# 在handle_timeout_error()中增加了周期时间控制
# 改进了错误恢复机制


import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)


class Test123():
    def setup_method(self, method):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--ignore-certificate-errors')
        self.option.add_experimental_option("detach", True)  # 防止浏览器自动关闭
        self.driver = None
        self.init_driver()
        self.vars = {}
        self.wait = WebDriverWait(self.driver, 30)  # 增加等待时间到30秒

    def init_driver(self):
        try:
            if self.driver:
                self.driver.quit()
            self.driver = webdriver.Chrome(options=self.option)
            self.driver.get("https://10.200.1.188/")
        except Exception as e:
            logging.error(f"初始化驱动失败: {str(e)}")
            time.sleep(60)  # 失败后等待1分钟
            self.init_driver()

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

    def handle_timeout_error(self):
        logging.info("正在处理超时错误...")
        elapsed_time = time.time() - self.cycle_start_time
        remaining_time = 2960 - elapsed_time  # 40分钟 = 2400秒
        if remaining_time > 0:
            logging.info(f"等待剩余时间: {remaining_time:.0f} 秒")
            time.sleep(remaining_time)
        self.init_driver()
        self.est_123()

    def login(self):
        try:
            time.sleep(2)
            username = self.wait_for_element(By.NAME, "username")
            username.send_keys("admin")
            password = self.wait_for_element(By.NAME, "password")
            password.send_keys("proav101")
            password.send_keys(Keys.ENTER)
        except Exception as e:
            logging.error(f"登录失败: {str(e)}")
            self.handle_timeout_error()

    def perform_upload_cycle(self, cycle_count):
        try:
            logging.info(f"开始执行第 {cycle_count} 个循环")
            self.cycle_start_time = time.time()

            # 2. 点击 "Device List"
            button = self.wait_for_element(By.LINK_TEXT, "Device List")
            button.click()
            time.sleep(5)

            self.turn_to_settings()

            # 上传V1
            logging.info(f"循环 {cycle_count}: 准备上传 V1")
            self.upload_file(r"E:\P-AVN-4_dev-1448-gd6b37119.tar")

            # 等待7分钟
            time.sleep(250)  # 7分钟 = 420秒
            self.turn_to_settings()

            # 上传V2
            logging.info(f"循环 {cycle_count}: 准备上传 V2")
            self.upload_file(r"E:\P-AVN-4_dev-1449-g174e833b.tar")

            # 10. 计算剩余等待时间以达到40分钟的循环周期
            elapsed_time = time.time() - self.cycle_start_time
            remaining_time = 2960 - elapsed_time  # 40分钟 = 2400秒
            if remaining_time > 0:
                logging.info(f"等待剩余时间: {remaining_time:.0f} 秒")
                time.sleep(remaining_time)

        except Exception as e:
            logging.error(f"循环执行过程中发生错误: {str(e)}")
            self.handle_timeout_error()

    def turn_to_settings(self):
        # 3.1 选中设备组
        root_checkbox = self.wait_for_element(By.XPATH,
                                              "//*[@id='root']/div/main/div[3]/table/thead/tr/th[1]/span/input")
        self.driver.execute_script("arguments[0].click();", root_checkbox)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", root_checkbox)
        time.sleep(1)
        test_checkbox = self.wait_for_element(By.XPATH,
                                              "//*[@id='root']/div/main/div[3]/table/tbody/tr[1]/td/table/thead/tr/th[1]/span/input")
        self.driver.execute_script("arguments[0].click();", test_checkbox)

        # 4. 进入设置页面
        second_element = self.wait_for_element(By.CSS_SELECTOR, ".css-o2hjg:nth-child(2)")
        second_element.click()

    def back_to_list(self):
        # 9. 返回页面
        back_button = self.wait_for_element(By.CSS_SELECTOR, ".css-1yjo05o > .MuiButton-outlined")
        back_button.click()

    def upload_file(self, file_path):
        try:
            # 5. 删除已有的文件
            error_icon = self.wait_for_element(By.CSS_SELECTOR, ".MuiSvgIcon-colorError > path")
            error_icon.click()

            # 6. 确认删除
            error_button = self.wait_for_element(By.CSS_SELECTOR, ".MuiButton-containedError")
            error_button.click()
            time.sleep(3)

            # 7. 上传文件
            file_input = self.wait_for_element(By.XPATH, "// *[ @ id = 'fwFile-file']")
            file_input.send_keys(file_path)
            logging.info(f"文件上传开始: {file_path}")

            # 等待上传完成
            time.sleep(20)

            # 8.确认升级
            update_button = self.wait_for_element(By.CSS_SELECTOR, "span > .MuiButton-root")
            update_button.click()
            update_check = self.wait_for_element(By.CSS_SELECTOR, ".MuiDialogActions-root > .MuiButton-contained")
            update_check.click()
            logging.info("升级中...")

            # 等待进度条自己删掉
            time.sleep(150)

            self.back_to_list()

        except Exception as e:
            logging.error(f"升级过程中发生错误: {str(e)}")
            self.handle_timeout_error()

    def est_123(self):
        self.login()
        cycle_count = 1
        while cycle_count <= 15:  # 执行15个循环
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
    while True:  # 永久循环
        try:
            test = Test123()
            test.setup_method(None)
            test.est_123()
            test.teardown_method(None)
            break  # 如果成功完成，则退出循环
        except Exception as e:
            logging.error(f"主程序发生错误: {str(e)}")
            time.sleep(60)  # 发生错误时等待1分钟后重试


if __name__ == "__main__":
    main()
