# 让gpt按照完整的步骤复用了代码，是逻辑完全、功能完全的代码
# 添加了15次的循环结构
# 在循环中加入了取消选中和重新选中设备组的步骤
# 实现了文件上传的交替（V1和V2）
# 添加了返回页面的操作
# 添加了循环计数的打印，方便追踪进度
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
        # 1. 等待页面加载，登陆
        time.sleep(2)
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

        # 3.1 初始选中设备组
        checkbox = self.driver.find_element(By.XPATH,
                                            "//*[@id='root']/div/main/div[3]/table/tbody/tr[4]/td/table/thead/tr/th[1]/span/input")
        self.driver.execute_script("arguments[0].click();", checkbox)

        # 开始循环
        for i in range(15):
            print(f"执行第 {i + 1} 次循环")

            # 3.2 取消选中设备组
            checkbox = self.driver.find_element(By.XPATH,
                                                "//*[@id='root']/div/main/div[3]/table/tbody/tr[4]/td/table/thead/tr/th[1]/span/input")
            self.driver.execute_script("arguments[0].click();", checkbox)

            # 3.3 重新选中设备组
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", checkbox)

            # 4. 进入设置页面
            second_element = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".css-o2hjg:nth-child(2)")))
            second_element.click()

            # 5. 删除已有的文件
            error_icon = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".MuiSvgIcon-colorError > path")))
            error_icon.click()

            # 6. 确认删除
            error_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".MuiButton-containedError")))
            error_button.click()

            time.sleep(5)

            # 7. 上传文件（交替上传V1和V2）
            file_input = self.driver.find_element(By.XPATH, "// *[ @ id = 'fwFile-file']")
            if i % 2 == 0:
                # 上传V1
                file_input.send_keys(r"E:\P-AVN-4_dev-r26584-p3-g82dd808f.tar")
            else:
                # 上传V2
                file_input.send_keys(r"E:\P-AVN-4_dev-1429-g0cce2e3b.tar")

            # 8. 等待上传
            time.sleep(30)

            # 9. 返回页面
            back_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".css-1yjo05o > .MuiButton-outlined")))  # 假设返回按钮使用这个选择器
            back_button.click()

            time.sleep(30)  # 等待30秒后进入下一次循环

        # 10. 关闭浏览器
        self.driver.close()


def main():
    test = Test123()
    test.setup_method(None)
    test.est_123()
    test.teardown_method(None)


if __name__ == "__main__":
    main()