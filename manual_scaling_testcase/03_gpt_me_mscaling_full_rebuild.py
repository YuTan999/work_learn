import queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
from threading import Timer
import sys
import msvcrt  # Windows系统下用于检测键盘输入
import select
import threading
import time
from queue import Queue, Empty
import concurrent.futures
import time
import os


class TestManualScaling:
    # TX和RX的配置映射
    DEVICE_CONFIG = {
        'tx': {
            'button_selector': ".MuiGrid-root:nth-child(3) > .MuiGrid-root:nth-child(1) .MuiButton-root",
            'confirm_button': ".MuiButton-containedSizeMedium",
            'resolution_xpath': "//div[3]/div/div/div/div/div[2]/div/div/div/div",
            'framerate_xpath': "//div/div/div/div/div[2]/div/div[2]/div/div",
        },
        'rx': {
            'button_selector': ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root",
            'confirm_button': ".css-1ec37i0",
            'resolution_xpath': "//div[3]/div/div/div/div/div[3]/div/div/div",
            'chroma_xpath': "//div[3]/div/div/div/div/div[4]/div/div/div",
            'framerate_xpath': "//div/div/div/div/div[3]/div[2]/div/div",
        }
    }

    def setup_method(self):
        chrome_driver_path = r'E:\jetbrain software\python\chromedriver-win64\chromedriver.exe'
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

        with open('config.txt', 'r') as file:
            self.ip_addresses = file.read().strip().split(',')
        print(self.ip_addresses)

        # 配置日志
        logging.basicConfig(
            filename='test_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


    def wait_for_input(self, timeout=10):
        print("\nEnter 1 for pass, 0 for fail ({}s timeout):".format(timeout), end='', flush=True)

        result = {'value': None}
        timeout_event = threading.Event()

        def get_input():
            try:
                print("get_input")
                result['value'] = input()
                print("get_input222222")
            except Exception as e:
                print(f"Error in get_input: {e}")
                logging.error(f"Exception in get_input: {e}")

        def timeout_callback():
            timeout_event.set()

        timer = threading.Timer(timeout, timeout_callback)
        timer.start()

        input_thread = threading.Thread(target=get_input)
        input_thread.start()

        # 等待输入线程完成或超时事件触发
        input_thread.join(timeout)

        timer.cancel()  # 取消定时器，防止资源泄漏

        if timeout_event.is_set():
            print("\nNo input received, defaulting to pass")
            return '1'

        if result['value'] in ['0', '1']:
            return result['value']

        return '1'


    def wait_for_input01_buhuichaoshi(self, timeout=5):
        print("\nEnter 1 for pass, 0 for fail (5s timeout):", end='', flush=True)

        def get_input():
            result = input()
            if result in ['0', '1']:
                return result
            return None

        # 使用 ThreadPoolExecutor 可以获取线程的返回值
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 提交任务并获取 Future 对象
            future = executor.submit(get_input)
            try:
                # 等待结果，设置超时时间
                result = future.result(timeout=timeout)
                print(result is None)
                print("result:")
                print(result)
                if result is not None:
                    return result
            except concurrent.futures.TimeoutError:
                pass

        print("\nNo input received, defaulting to pass")
        return '1'
    def wait_for_input_xianchengyouwenti(self,timeout=5):
        print("\nEnter 1 for pass, 0 for fail (5s timeout):", end='', flush=True)
        def get_input():
            return input()

        input_str = [None]  # 使用列表存储输入值

        def input_thread():
            try:
                print("222222222222222222222222222222")
                result = get_input()
                print("result:  "+result)
                if result in ['0', '1']:
                    input_str[0] = result
                # print("线程里")
                print(input_str)
            except:
                pass

        thread = threading.Thread(target=input_thread)
        thread.daemon = True  # 设置为守护线程
        thread.start()
        time.sleep(5)  # 添加短暂延迟，确保input_thread有时间开始执行
        thread.join(timeout)  # 等待指定的超时时间

        # 使用循环检查输入值，直到超时或收到输入
        start_time = time.time()
        while time.time() - start_time < timeout:
            print(input_str)
            if input_str[0] is not None:  # 如果已经有输入值
                break
            time.sleep(0.1)  # 短暂休眠，避免过度消耗CPU

        # print("线程外")
        print(input_str)
        if input_str[0] is None:
            print("\nNo input received, defaulting to pass")
            return '1'
        return input_str[0]
    # 添加一个等待输入的函数
    def wait_for_input3_jiancebudaomsvcrt(self, timeout=20):
        start_time = time.time()
        input_str = ''
        print("\nEnter 1 for pass, 0 for fail (5s timeout):", end='', flush=True)

        while (time.time() - start_time) < timeout:
            # 检查是否有键盘输入
            if msvcrt.kbhit():
                char = sys.stdin.read(1)  # 使用sys.stdin.read(1)替代msvcrt.getch()
                if char in ['0', '1']:
                    input_str = char
                    print(char)
                    break
                elif char == '\r':  # Enter键
                    break

        if not input_str:  # 如果超时没有输入
            print("\nNo input received, defaulting to pass")
            return '1'

        return input_str

    def wait_for_input_windows(self, timeout=10, default='1'):
        start_time = time.time()
        print("\nEnter 1 for pass, 0 for fail ({}s timeout):".format(timeout), end='', flush=True)
        input = ''
        read_f = msvcrt.getche
        input_check = msvcrt.kbhit
        if not sys.stdin.isatty():
            read_f = lambda: sys.stdin.read(1)
            input_check = lambda: True
        while True:
            if input_check():
                chr_or_str = read_f()
                try:
                    if ord(chr_or_str) == 13:  # enter_key
                        break
                    elif ord(chr_or_str) >= 32:  # space_char
                        input += chr_or_str
                except:
                    input = chr_or_str
                    break  # read line, not char...
            if len(input) == 0 and (time.time() - start_time) > timeout:
                break
        if len(input) > 0:
            return input
        else:
            return default

    def wait_for_input0(self, timeout=10):
        print("\nEnter 1 for pass, 0 for fail ({}s timeout):".format(timeout), end='', flush=True)

        result = {'value': None}

        def get_input():
            try:
                print("get_input")
                result['value'] = input("这对吗？")
                print("get_input222222")

            except Exception as e:
                print(f"Error in get_input: {e}")
                logging.error(f"Exception in get_input: {e}")



        timer = Timer(timeout, lambda: print('\nNo input received, defaulting to pass'))
        timer.start()

        try:
            get_input()
            timer.cancel()
            print("try")
        except:
            timer.cancel()
            return '1'
            print("except")

        print(result)
        if result['value'] in ['0', '1']:
            return result['value']

        return '1'

    def wait_for_input2(self, timeout=10):
        start_time = time.time()
        input_str = ''
        print("\nEnter 1 for pass, 0 for fail ({}s timeout):".format(timeout), end='', flush=True)

        while (time.time() - start_time) < timeout:
            # 使用 select 模块检测输入
            if select.select([sys.stdin], [], [], 0.1)[0]:
                char = sys.stdin.read(1)  # 读取单个字符
                if char in ['0', '1']:
                    input_str = char
                    print(char)
                    break
                elif char == '\r':  # Enter键
                    break

        if not input_str:  # 如果超时没有输入
            print("\nNo input received, defaulting to pass")
            return '1'

        return input_str
    def teardown_method(self):
        self.driver.quit()

    def open_page(self, ip_address):
        # self.driver.get(f"http://{ip_address}/")
        # USERNAME_INPUT = (By.NAME, "username")
        # if self.is_element_present(USERNAME_INPUT):
        #     self.driver.find_element(By.NAME, "username").send_keys("admin")
        #     self.driver.find_element(By.NAME, "username").send_keys(Keys.ENTER)
        time.sleep(2)

    def select_option_generic(self, device_type, xpath_key, value):
        config = self.DEVICE_CONFIG[device_type]

        # 点击设置按钮
        button = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, config['button_selector'])))
        button.click()
        time.sleep(1)

        # 选择选项
        menu = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, config[xpath_key])))
        menu.click()
        time.sleep(1)

        option = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f".MuiMenuItem-root:nth-child({value}")))
        option.click()

        # 确认
        confirm = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, config['confirm_button'])))
        confirm.click()
        time.sleep(0.3)

    def tx_setup(self):
        button = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, self.DEVICE_CONFIG['tx']['button_selector'])))
        button.click()
        time.sleep(2)

        # 设置压缩选项
        for compress in ['lightCompress', 'highCompress']:
            element = self.driver.find_element(By.NAME, compress)
            if not element.is_selected():
                element.click()

        # 设置宽高比
        ratio_menu = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/div/div[3]/div/div/div")))
        ratio_menu.click()
        time.sleep(1)
        ratio_option = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)")))
        ratio_option.click()

        confirm = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, self.DEVICE_CONFIG['tx']['confirm_button'])))
        confirm.click()

    def rx_setup(self):
        button = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, self.DEVICE_CONFIG['rx']['button_selector'])))
        button.click()
        time.sleep(2)

        # 设置低延迟
        self.driver.find_element(
            By.XPATH, "(//input[@name='inputselectionSeamlessSwitchingState'])[2]").click()

        # 设置手动模式
        mode_menu = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/div/div[2]/div/div")))
        mode_menu.click()
        time.sleep(1)
        mode_option = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f".MuiMenuItem-root:nth-child(2)")))
        mode_option.click()

        # 设置宽高比
        ratio_menu = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/div/div[5]/div/div")))
        ratio_menu.click()
        time.sleep(1)
        ratio_option = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)")))
        ratio_option.click()

        confirm = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, self.DEVICE_CONFIG['rx']['confirm_button'])))
        confirm.click()

    def update_tx_settings(self, resolution_value=None, framerate_value=None):
        if resolution_value:
            self.select_option_generic('tx', 'resolution_xpath', resolution_value)
        if framerate_value:
            self.select_option_generic('tx', 'framerate_xpath', framerate_value)

    def update_rx_settings(self, resolution_value=None, chroma_value=None, framerate_max=None, tx_resolution=None, tx_framerate=None):
        # if resolution_value:
        #     self.select_option_generic('rx', 'resolution_xpath', resolution_value)
        # if chroma_value:
        #     self.select_option_generic('rx', 'chroma_xpath', chroma_value)
        if framerate_max:
            for i in range(1, framerate_max + 1):
                # self.select_option_generic('rx', 'framerate_xpath', i)

                print(tx_resolution, tx_framerate,resolution_value,chroma_value,i)
                result = self.wait_for_input_windows()
                print("result:")
                print(result)
                if result == '0':
                    print("\nPlease enter the issue description:")
                    issue = input()
                    logging.error(f"""
                Test Failed:
                TX Settings:
                - Resolution: {tx_resolution}
                - Framerate: {tx_framerate}
                RX Settings:
                - Resolution: {resolution_value}
                - Chroma: {chroma_value}
                - Current Framerate: {i}
                Issue Description: {issue}
                                """)

                time.sleep(7 if i == framerate_max else 8)

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except Exception:
            return False


def main():
    test = TestManualScaling()
    test.setup_method()

    # 初始设置
    # test.open_page(test.ip_addresses[0])
    # test.tx_setup()
    # test.open_page(test.ip_addresses[1])
    # test.rx_setup()

    test_config = {
        '3840': {'resolution': 1, 'framerates': [4, 3, 2, 1]},
        '1080': {'resolution': 2, 'framerates': [4, 3, 2, 1]},
        '720': {'resolution': 3, 'framerates': [2, 1]}
    }

    rx_test_sequence = [
        {'resolution': 1, 'chroma': 1, 'name': "3840 yuv"},
        {'resolution': 1, 'chroma': 2, 'name': "3840 rgb"},
        {'resolution': 2, 'chroma': 2, 'name': "1080 rgb"},
        {'resolution': 2, 'chroma': 1, 'name': "1080 yuv"},
        {'resolution': 3, 'chroma': 1, 'name': "720 yuv"},
        {'resolution': 3, 'chroma': 2, 'name': "720 rgb"}
    ]

    for resolution, config in test_config.items():
        # test.open_page(test.ip_addresses[0])
        # test.update_tx_settings(resolution_value=config['resolution'])

        for framerate in config['framerates']:
            # print(f"Testing {resolution} with framerate {framerate}")
            # test.open_page(test.ip_addresses[0])
            # test.update_tx_settings(framerate_value=framerate)

            # test.open_page(test.ip_addresses[1])
            for rx_test in rx_test_sequence:
                # print(f"Testing RX: {rx_test['name']}")
                test.update_rx_settings(
                    resolution_value=rx_test['resolution'],
                    chroma_value=rx_test['chroma'],
                    framerate_max=4 if rx_test['resolution'] < 3 else 2,
                    tx_resolution = resolution,  # 当前TX的分辨率
                    tx_framerate = framerate  # 当前TX的帧率
                )

    test.teardown_method()


if __name__ == "__main__":
    main()
