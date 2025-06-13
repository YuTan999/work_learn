# 艰苦地把基础步骤跑过了,是逻辑完全、功能不全的代码
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Test123():
    def setup_method(self, method):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.get("https://10.200.1.188/")
        self.vars = {}
        self.wait = WebDriverWait(self.driver, 10)  # 设置等待时间为10秒

    def teardown_method(self, method):
        self.driver.quit()

    def est_123(self):
        time.sleep(2)
        # 1. 等待页面加载，登陆
        # 输入用户名
        self.driver.find_element(By.NAME, "username").send_keys("admin")
        # 输入密码
        self.driver.find_element(By.NAME, "password").send_keys("proav101")
        # 提交表单
        self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

        # 2. 点击 "Device List"
        button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Device List")))
        button.click()

        time.sleep(5)
        #
        # self.driver.find_element(By.XPATH,
        #                          "//*[@id=\"root\"]/div/main/div[3]/table/tbody/tr[3]/td/table/thead/tr/th[1]/span/input").click()
        # 点击第三行的开关
        # switchs = self.wait.until(EC.visibility_of_element_located(
        #     (By.CSS_SELECTOR, ".MuiTableRow-root:nth-child(1) .MuiTableHead-root .PrivateSwitchBase-input")))
        # switchs.click()
        # 如果 click() 方法无法正常工作，可以使用 JavaScript 来直接设置 checkbox 的状态：
        # 3. 选中设备组
        checkbox = self.driver.find_element(By.XPATH,
                                            "//*[@id='root']/div/main/div[3]/table/tbody/tr[4]/td/table/thead/tr/th[1]/span/input")
        self.driver.execute_script("arguments[0].click();", checkbox)
        # 4. 进入设置页面
        # 点击第二个元素
        second_element = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".css-o2hjg:nth-child(2)")))
        second_element.click()

        # # 点击 "Upload"
        # upload_button = self.wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, "//span[contains(.,'Upload')]")))
        # upload_button.click()
        time.sleep(5)
        # 点击 Upload 按钮
        # file_input = self.driver.find_element(By.XPATH, "// *[ @ id = 'fwFile-file']")
        # (By.XPATH, "//span[contains(.,'Upload')]")))

        # file_input.send_keys(r"E:\P-AVN-4_dev-1429-g0cce2e3b.tar")
        # time.sleep(30)

        # # 5. 删除已有的文件V1
        # # 点击错误图标
        # error_icon = self.wait.until(EC.element_to_be_clickable(
        #     (By.CSS_SELECTOR, ".MuiSvgIcon-colorError > path")))
        # error_icon.click()
        # # 6.确认删除
        # # 点击错误按钮
        # error_button = self.wait.until(EC.element_to_be_clickable(
        #     (By.CSS_SELECTOR, ".MuiButton-containedError")))
        # error_button.click()
        #
        # time.sleep(5)
        # # 7. 上传文件
        # # 7.2 上传文件V2
        # file_input = self.driver.find_element(By.XPATH, "// *[ @ id = 'fwFile-file']")
        # # 7.1 这是上传V1的代码
        # # file_input.send_keys(r"E:\P-AVN-4_dev-r26584-p3-g82dd808f.tar")

        # file_input.send_keys(r"E:\P-AVN-4_dev-1429-g0cce2e3b.tar")
        output = self.driver.find_element(By.CSS_SELECTOR, ".css-1yjo05o > .MuiButton-outlined")
        output.click()
        # 8.等待上传
        time.sleep(30)
        # 10. 关闭浏览器
        self.driver.close()


def main():
    test = Test123()
    test.setup_method(None)
    test.est_123()
    test.teardown_method(None)


if __name__ == "__main__":
    main()
