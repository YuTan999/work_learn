import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Test123():
    def setup_method(self, method):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.get("https://10.200.8.226/")
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_123(self):
        time.sleep(500)
        # Test name: 123
        # Step # | name | target | value
        # 1 | open | / |
        # 3 | type | name=username | admin
        self.driver.find_element(By.NAME, "username").send_keys("admin")
        # 4 | type | name=password | proav101
        self.driver.find_element(By.NAME, "password").send_keys("proav101")
        # 5 | sendKeys | name=password | ${KEY_ENTER}
        self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
        # 2 | click | linkText=Device List |
        self.driver.find_element(By.LINK_TEXT, "Device List").click()
        # 2 | click | linkText=Device List |
        self.driver.find_element(By.LINK_TEXT, "Device List").click()
        # 3 | click | css=.MuiTableRow-root:nth-child(3) .MuiTableHead-root .PrivateSwitchBase-input |
        self.driver.find_element(By.CSS_SELECTOR,
                                 ".MuiTableRow-root:nth-child(3) .MuiTableHead-root .PrivateSwitchBase-input").click()
        # 4 | click | css=.css-o2hjg:nth-child(2) |
        self.driver.find_element(By.CSS_SELECTOR, ".css-o2hjg:nth-child(2)").click()
        # 5 | click | xpath=//span[contains(.,'Upload')] |
        self.driver.find_element(By.XPATH, "//span[contains(.,\'Upload\')]").click()
        # 6 | click | css=.MuiSvgIcon-colorError > path |
        self.driver.find_element(By.CSS_SELECTOR, ".MuiSvgIcon-colorError > path").click()