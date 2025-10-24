# coding=gbk
import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Test123():
    def setup_method(self, method):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.get("http://10.200.0.108/")
        self.vars = {}
        self.wait = WebDriverWait(self.driver, 10)  # 设置等待时间为10秒

    def wait_for_element(self, by, value, timeout=30):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return self.wait_for_element(by, value, timeout)

    def teardown_method(self, method):
        self.driver.quit()

    def est_123(self):
        time.sleep(3)
        username = self.wait_for_element(By.XPATH, "//div[@id='app']/div/div/div/div[2]/div/form/div/div/fieldset/div/div/input")
        username.send_keys("admin")
        password = self.wait_for_element(By.XPATH, "//input[@type='password']")
        password.send_keys("Sencore123")
        password.send_keys(Keys.ENTER)
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, ".is-active .el-menu-item:nth-child(6)").click()
        time.sleep(3)
        # 1.  进入设置
        self.driver.find_element(By.CSS_SELECTOR, ".el-button--text:nth-child(2) > span").click()
        time.sleep(3)
        # 2.  选中设备
        self.driver.find_element(By.CSS_SELECTOR, ".mt20 .el-checkbox__inner").click()
        time.sleep(3)
        # 3.  这一步是点击开关，首次进入设置时开关是默认打开的
        self.driver.find_element(By.CSS_SELECTOR, ".el-switch__core").click()
        time.sleep(3)
        # 4.  apply
        self.driver.find_element(By.CSS_SELECTOR, ".el-dialog__footer:nth-child(3) .el-button--primary").click()


def main():
    test = Test123()
    test.setup_method(None)
    test.est_123()
    test.teardown_method(None)


if __name__ == "__main__":
    main()
