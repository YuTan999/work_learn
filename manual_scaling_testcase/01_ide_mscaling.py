# 1.直接从Selenium IDE导出的代码，跑不了
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestManualscaling():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_19turnto3840(self):
    # Test name: 1.9 turn to 3840
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://10.200.8.40/")
    # 2 | setWindowSize | 974x727 | 
    self.driver.set_window_size(974, 727)
    # 3 | runScript | window.scrollTo(0,0) | 
    self.driver.execute_script("window.scrollTo(0,0)")
    # 4 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root:nth-child(1) .css-15vhhhd:nth-child(1) .MuiSvgIcon-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root:nth-child(1) .css-15vhhhd:nth-child(1) .MuiSvgIcon-root:nth-child(1)").click()
    # 5 | mouseDown | id=mui-86 | 
    element = self.driver.find_element(By.ID, "mui-86")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 6 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 7 | pause | 300 | 
    time.sleep(0.3)
    # 8 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 9 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 10 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 11 | close |  | 
    self.driver.close()
  
  def test_1138401080yuvframechange(self):
    # Test name: 1.1.3840-1080yuvframe change 
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://10.200.8.40/")
    # 2 | setWindowSize | 1411x1032 | 
    self.driver.set_window_size(1411, 1032)
    # 3 | pause | 500 | 
    time.sleep(0.5)
    # 4 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 5 | mouseDown | id=mui-88 | 
    element = self.driver.find_element(By.ID, "mui-88")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 6 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 7 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 8 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 9 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 10 | pause | 5000 | 
    time.sleep(5)
    # 11 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 12 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 13 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 14 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 15 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 16 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 17 | pause | 25000 | 
    time.sleep(25)
    # 18 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 19 | mouseDown | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    element = self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 20 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 21 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 22 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 23 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 24 | pause | 25000 | 
    time.sleep(25)
    # 25 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 26 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 27 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 28 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 29 | click | css=.MuiMenuItem-root:nth-child(3) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(3)").click()
    # 30 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 31 | pause | 20000 | 
    time.sleep(20)
    # 32 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 33 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 34 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 35 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 36 | click | css=.MuiMenuItem-root:nth-child(4) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(4)").click()
    # 37 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 38 | pause | 25000 | 
    time.sleep(25)
    # 39 | close |  | 
    self.driver.close()
  
  def test_1238401080rgbframechange(self):
    # Test name: 1.2.3840-1080-rgb-frame change
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://10.200.8.40/")
    # 2 | setWindowSize | 1411x1032 | 
    self.driver.set_window_size(1411, 1032)
    # 3 | pause | 500 | 
    time.sleep(0.5)
    # 4 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 5 | mouseDown | id=mui-88 | 
    element = self.driver.find_element(By.ID, "mui-88")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 6 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 7 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 8 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 9 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 10 | pause | 5000 | 
    time.sleep(5)
    # 11 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 12 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 13 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 14 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 15 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 16 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 17 | pause | 25000 | 
    time.sleep(25)
    # 18 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 19 | mouseDown | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    element = self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 20 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 21 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 22 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 23 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 24 | pause | 20000 | 
    time.sleep(20)
    # 25 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 26 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 27 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 28 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 29 | click | css=.MuiMenuItem-root:nth-child(3) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(3)").click()
    # 30 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 31 | pause | 20000 | 
    time.sleep(20)
    # 32 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 33 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 34 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 35 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 36 | click | css=.MuiMenuItem-root:nth-child(4) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(4)").click()
    # 37 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 38 | pause | 25000 | 
    time.sleep(25)
    # 39 | close |  | 
    self.driver.close()
  
  def test_13turnto1080(self):
    # Test name: 1.3turn to1080
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://10.200.8.40/")
    # 2 | setWindowSize | 974x727 | 
    self.driver.set_window_size(974, 727)
    # 3 | runScript | window.scrollTo(0,0) | 
    self.driver.execute_script("window.scrollTo(0,0)")
    # 4 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 5 | mouseDown | id=mui-86 | 
    element = self.driver.find_element(By.ID, "mui-86")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 6 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 7 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 8 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 9 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 10 | close |  | 
    self.driver.close()
  
  def test_1438401080rgbframechange(self):
    # Test name: 1.4.3840-1080-rgb-frame change 
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://10.200.8.40/")
    # 2 | setWindowSize | 1411x1032 | 
    self.driver.set_window_size(1411, 1032)
    # 3 | pause | 500 | 
    time.sleep(0.5)
    # 4 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 5 | mouseDown | id=mui-88 | 
    element = self.driver.find_element(By.ID, "mui-88")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 6 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 7 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 8 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 9 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 10 | pause | 5000 | 
    time.sleep(5)
    # 11 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 12 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 13 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 14 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 15 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 16 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 17 | pause | 25000 | 
    time.sleep(25)
    # 18 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 19 | mouseDown | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    element = self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 20 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 21 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 22 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 23 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 24 | pause | 20000 | 
    time.sleep(20)
    # 25 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 26 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 27 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 28 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 29 | click | css=.MuiMenuItem-root:nth-child(3) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(3)").click()
    # 30 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 31 | pause | 20000 | 
    time.sleep(20)
    # 32 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 33 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 34 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 35 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 36 | click | css=.MuiMenuItem-root:nth-child(4) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(4)").click()
    # 37 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 38 | pause | 25000 | 
    time.sleep(25)
    # 39 | close |  | 
    self.driver.close()
  
  def test_1538401080yuvframechange(self):
    # Test name: 1.5.3840-1080yuvframe change 
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://10.200.8.40/")
    # 2 | setWindowSize | 1411x1032 | 
    self.driver.set_window_size(1411, 1032)
    # 3 | pause | 500 | 
    time.sleep(0.5)
    # 4 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 5 | mouseDown | id=mui-88 | 
    element = self.driver.find_element(By.ID, "mui-88")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 6 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 7 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 8 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 9 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 10 | pause | 5000 | 
    time.sleep(5)
    # 11 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 12 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 13 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 14 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 15 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 16 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 17 | pause | 25000 | 
    time.sleep(25)
    # 18 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 19 | mouseDown | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    element = self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 20 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 21 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 22 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 23 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 24 | pause | 25000 | 
    time.sleep(25)
    # 25 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 26 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 27 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 28 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 29 | click | css=.MuiMenuItem-root:nth-child(3) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(3)").click()
    # 30 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 31 | pause | 20000 | 
    time.sleep(20)
    # 32 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 33 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 34 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 35 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 36 | click | css=.MuiMenuItem-root:nth-child(4) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(4)").click()
    # 37 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 38 | pause | 25000 | 
    time.sleep(25)
    # 39 | close |  | 
    self.driver.close()
  
  def test_16turnto720(self):
    # Test name: 1.6 turnto 720
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://10.200.8.40/")
    # 2 | setWindowSize | 974x727 | 
    self.driver.set_window_size(974, 727)
    # 3 | runScript | window.scrollTo(0,0) | 
    self.driver.execute_script("window.scrollTo(0,0)")
    # 4 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 5 | mouseDown | id=mui-86 | 
    element = self.driver.find_element(By.ID, "mui-86")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 6 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 7 | pause | 200 | 
    time.sleep(0.2)
    # 8 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 9 | click | css=.MuiMenuItem-root:nth-child(3) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(3)").click()
    # 10 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 11 | close |  | 
    self.driver.close()
  
  def test_17720yuvframechange(self):
    # Test name: 1.7.720yuvframe change
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://10.200.8.40/")
    # 2 | setWindowSize | 1411x1032 | 
    self.driver.set_window_size(1411, 1032)
    # 3 | pause | 500 | 
    time.sleep(0.5)
    # 4 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 5 | mouseDown | id=mui-88 | 
    element = self.driver.find_element(By.ID, "mui-88")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 6 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 7 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 8 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 9 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 10 | pause | 4000 | 
    time.sleep(4)
    # 11 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 12 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 13 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 14 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 15 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 16 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 17 | pause | 20000 | 
    time.sleep(20)
    # 18 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 19 | mouseDown | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    element = self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 20 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 21 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 22 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 23 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 24 | pause | 20000 | 
    time.sleep(20)
    # 25 | close |  | 
    self.driver.close()
  
  def test_18720rgbframechange(self):
    # Test name: 1.8.720rgbframe change 
    # Step # | name | target | value
    # 1 | open | / | 
    self.driver.get("http://10.200.8.40/")
    # 2 | setWindowSize | 1411x1032 | 
    self.driver.set_window_size(1411, 1032)
    # 3 | pause | 500 | 
    time.sleep(0.5)
    # 4 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 5 | mouseDown | id=mui-88 | 
    element = self.driver.find_element(By.ID, "mui-88")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 6 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 7 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 8 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 9 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 10 | pause | 5000 | 
    time.sleep(5)
    # 11 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 12 | click | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div").click()
    # 13 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 14 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 15 | click | css=.MuiMenuItem-root:nth-child(2) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(2)").click()
    # 16 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 17 | pause | 25000 | 
    time.sleep(25)
    # 18 | click | css=.MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiGrid-root:nth-child(1) > .MuiPaper-root .css-15vhhhd .MuiButton-root").click()
    # 19 | mouseDown | xpath=//div/div/div/div/div[3]/div[2]/div/div | 
    element = self.driver.find_element(By.XPATH, "//div/div/div/div/div[3]/div[2]/div/div")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).click_and_hold().perform()
    # 20 | mouseUp | css=.MuiBackdrop-invisible | 
    element = self.driver.find_element(By.CSS_SELECTOR, ".MuiBackdrop-invisible")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).release().perform()
    # 21 | click | css=body | 
    self.driver.find_element(By.CSS_SELECTOR, "body").click()
    # 22 | click | css=.MuiMenuItem-root:nth-child(1) | 
    self.driver.find_element(By.CSS_SELECTOR, ".MuiMenuItem-root:nth-child(1)").click()
    # 23 | click | css=.css-1ec37i0 | 
    self.driver.find_element(By.CSS_SELECTOR, ".css-1ec37i0").click()
    # 24 | pause | 25000 | 
    time.sleep(25)
    # 25 | close |  | 
    self.driver.close()
  
