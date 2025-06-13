# 2. gpt完善过的完整代码，以及自己的调整，能跑通
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class TestManualScaling:
    def setup_method(self):
        chrome_driver_path = r'E:\jetbrain software\python\chromedriver-win64\chromedriver.exe'
        service = Service(chrome_driver_path)
        # 初始化WebDriver
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        self.open_page()

    def teardown_method(self):
        self.driver.close()
        self.driver.quit()

    def open_page(self):
        self.driver.get("http://10.200.0.74/")
        self.driver.find_element(By.NAME, "username").send_keys("admin")
        self.driver.find_element(By.NAME, "username").send_keys(Keys.ENTER)
        time.sleep(1)

    def select_option(self, xpath, value):
        # 点击打开下拉菜单
        button = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root")))
        button.click()
        time.sleep(3)

        # 点击下拉菜单
        menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"{xpath}")))
        menu.click()
        time.sleep(1)

        # 选择选项
        option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".MuiMenuItem-root:nth-child({value})")))
        option.click()

        # 点击确认按钮
        confirm = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1ec37i0")))
        confirm.click()

    def update_resolution(self, value):
        # 分辨率
        self.select_option("//div[3]/div/div/div/div/div[3]/div/div/div", value)
        time.sleep(0.3)

    def update_chroma(self, value):
        # 色彩
        self.select_option("//div[3]/div/div/div/div/div[4]/div/div/div", value)
        time.sleep(0.3)

    def update_framerate(self, value):
        # 帧率
        for i in range(1, value + 1):
            self.select_option("//div/div/div/div/div[3]/div[2]/div/div", i)
            time.sleep(15 if i == value else 17)


def main():
    test = TestManualScaling()

    test.setup_method()
    print("Running test 1: 1.9 turn to 3840")
    test.update_resolution(1)
    print("Running test 2: 1.1 3840-1080 yuv frame change")
    test.update_chroma(1)
    test.update_framerate(4)
    print("Running test 3: 1.2 3840-1080 rgb frame change")
    test.update_chroma(2)
    test.update_framerate(4)
    test.teardown_method()

    test.setup_method()
    print("Running test 4: 1.3 turn to 1080")
    test.update_resolution(2)
    print("Running test 5: 1.4 3840-1080 rgb frame change")
    test.update_chroma(2)
    test.update_framerate(4)
    print("Running test 6: 1.5 3840-1080 yuv frame change")
    test.update_chroma(1)
    test.update_framerate(4)
    test.teardown_method()

    test.setup_method()
    print("Running test 7: 1.6 turn to 720")
    test.update_resolution(3)
    print("Running test 8: 1.7 720 yuv frame change")
    test.update_chroma(1)
    test.update_framerate(2)
    print("Running test 9: 1.8 720 rgb frame change")
    test.update_chroma(2)
    test.update_framerate(2)
    test.teardown_method()


if __name__ == "__main__":
    main()
