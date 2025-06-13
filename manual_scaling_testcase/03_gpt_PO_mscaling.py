import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 基础封装层
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def find_element(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.find_element(locator).click()

    def send_keys(self, locator, text):
        self.find_element(locator).send_keys(text)

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except Exception:
            return False


# PO页面对象层
class ScalingPage(BasePage):
    # 定义页面元素
    USERNAME_INPUT = (By.NAME, "username")
    DROPDOWN_BUTTON = (By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, ".css-1ec37i0")
    RESOLUTION_DROPDOWN = "//div[3]/div/div/div/div/div[3]/div/div/div"
    CHROMA_DROPDOWN = "//div[3]/div/div/div/div/div[4]/div/div/div"
    FRAMERATE_DROPDOWN = "//div/div/div/div/div[3]/div[2]/div/div"

    def login(self, username):
        if self.is_element_present(self.USERNAME_INPUT):
            self.send_keys(self.USERNAME_INPUT, username)
            self.send_keys(self.USERNAME_INPUT, Keys.ENTER)
            time.sleep(1)

    def select_option(self, xpath, value):
        self.click(self.DROPDOWN_BUTTON)
        time.sleep(3)
        self.click((By.XPATH, xpath))
        time.sleep(1)
        self.click((By.CSS_SELECTOR, f".MuiMenuItem-root:nth-child({value})"))
        self.click(self.CONFIRM_BUTTON)

    def update_resolution(self, value):
        self.select_option(self.RESOLUTION_DROPDOWN, value)
        time.sleep(0.3)

    def update_chroma(self, value):
        self.select_option(self.CHROMA_DROPDOWN, value)
        time.sleep(0.3)

    def update_framerate(self, value):
        for i in range(1, value + 1):
            self.select_option(self.FRAMERATE_DROPDOWN, i)
            time.sleep(15 if i == value else 17)


# TestCase测试用例层
# class TestManualScaling:
#     @pytest.fixture(scope="function")
#     def setup(self):
#         self.driver = webdriver.Chrome()
#         self.driver.maximize_window()
#         self.scaling_page = ScalingPage(self.driver)
#         self.driver.get("http://10.200.8.40/")
#         self.scaling_page.login("admin")
#         yield
#         self.driver.quit()
#
#     @pytest.mark.parametrize("test_name, resolution, chroma, framerate", [
#         ("1.0 turn to 3840", 1, None, None),
#         ("1.1 3840 yuv frame change", None, 1, 4),
#         ("1.2 3840 rgb frame change", None, 2, 4),
#         ("1.3 turn to 1080", 2, None, None),
#         ("1.4 1080 rgb frame change", None, 2, 4),
#         ("1.5 1080 yuv frame change", None, 1, 4),
#         ("1.6 turn to 720", 3, None, None),
#         ("1.7 720 yuv frame change", None, 1, 2),
#         ("1.8 720 rgb frame change", None, 2, 2),
#     ])
#     def test_scaling(self, setup, test_name, resolution, chroma, framerate):
#         print(f"Running test: {test_name}")
#         if resolution:
#             self.scaling_page.update_resolution(resolution)
#         if chroma:
#             self.scaling_page.update_chroma(chroma)
#         if framerate:
#             self.scaling_page.update_framerate(framerate)

class TestManualScaling:
    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.quit()

    @pytest.fixture(scope="function")
    def scaling_page(self, driver):
        page = ScalingPage(driver)
        driver.get("http://10.200.0.74/")
        page.login("admin")
        return page

    @pytest.mark.parametrize("test_group", [
        [
            ("1.0 turn to 3840", 1, None, None),
            ("1.1 3840 yuv frame change", None, 1, 4),
            ("1.2 3840 rgb frame change", None, 2, 4)
        ],
        [
            ("1.3 turn to 1080", 2, None, None),
            ("1.4 1080 rgb frame change", None, 2, 4),
            ("1.5 1080 yuv frame change", None, 1, 4)
        ],
        [
            ("1.6 turn to 720", 3, None, None),
            ("1.7 720 yuv frame change", None, 1, 2),
            ("1.8 720 rgb frame change", None, 2, 2)
        ]
    ])
    def test_scaling_group(self, driver, scaling_page, test_group):
        for test_name, resolution, chroma, framerate in test_group:
            print(f"Running test: {test_name}")
            if resolution:
                scaling_page.update_resolution(resolution)
            if chroma:
                scaling_page.update_chroma(chroma)
            if framerate:
                scaling_page.update_framerate(framerate)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
