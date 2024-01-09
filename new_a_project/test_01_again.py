import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://10.200.0.7")
driver.maximize_window()

# 元素定位
# id,name,class
driver.find_element(By.NAME,'username').send_keys("admin")
# tag_name
inputel = driver.find_elements(By.TAG_NAME,'input')
inputel[1].send_keys("mpeg101")
# link_text\partial_link_text?

# Xpath
# 相对路径·下标从1开始？
# @id（无需值）区分两个class重复的元素
driver.find_element(By.XPATH,'//button[1]').click()
driver.find_element(By.XPATH,'//button[@id]').click()
time.sleep(3)
# 文本（精确）
# driver.find_element(By.XPATH,'//*[text()="IP IN"]').click()


# Class
# 右侧info
# driver.find_element(By.CSS_SELECTOR,'.MuiTouchRipple-root').click()

driver.quit()