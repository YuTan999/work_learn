import time
from enum import Enum

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
'''
这里是功能模块，一般不要修改，请继续往下阅读
'''

# 等到目标ID出现为止,每0.5s检测一次，默认超时时间为10s
def waitIdTarget( driver, str, timeout=10 ):
  try:
   WebDriverWait(driver, timeout, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="' + str + '"]')))
   return 0
  except:
   print( "load Id[" + str + "] failed" )
   return 1

# 等到目标ID消失为止,每0.5s检测一次，默认超时时间为10s
def waitWithoutIdTarget( driver, str, timeout=10 ):
  try:
   WebDriverWait(driver, timeout, 0.5).until_not(EC.presence_of_element_located((By.XPATH, '//*[@id="' + str + '"]')))
   return 0
  except:
   print( "exit Id[" + str + "] failed" )
   return 1

# 选择对应的schema，返回一个对象
def selectSchema( driver, str ):
  schemaObj = driver.find_element_by_xpath("//tr/td/div[contains(text(),'"+ str + "')]")
  return schemaObj

# 选择对应的schema，返回一个对象
def selectSchemaOption( driver, str ):
  schemaObj = driver.find_element_by_xpath("//table/tbody/tr/td/div[contains(text(),'"+ str + "')]/../../td[3]/div")
  return schemaObj

# 获取schema一个选项的值
def getSelectSchemaOptionValue( driver, str ):
  schemaObj = selectSchemaOption( driver, str )
  return schemaObj.text

# 设置schema一个选项的值
def setSelectSchemaOptionValue( driver, str, value ):
  schemaObj = selectSchemaOption( driver, str )
  schemaObj.click()
  schemaObj2 = driver.find_element_by_xpath("//input[@id]")
  schemaObj2.send_keys(value)
  time.sleep(1)
  driver.find_element_by_id("applyButton-btnInnerEl").click();
  time.sleep(1)

# 点击刷新按键
def refreshClick( driver ):
  driver.find_element_by_id("refreshButton-btnEl").click();
  time.sleep(1)

# 等待出现某个字符串
# 等到目标ID出现text的内容为止,每0.5s检测一次，默认超时时间为10s
def waitIdAndTextTarget( driver, id, text, timeout=10 ):
  try:
   WebDriverWait(driver, timeout, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="' + id + '"][contains(text(),"'+ text + '")]')))
   return 0
  except:
   print( "load [" + id + "][" + text + "]failed" )
   return 1




#-----------------------------------sencore 升级自动化脚本---------------------------------------
'''
大致原理是：
1.登录+输入密码
2.选择升级文件，并传送升级文件，异常时退出
3.点击yes升级，或者同版本升级
4.等待升级成功反馈
'''
class Upgrade(Enum):
	# 为序列值指定value值
	Success = 0 
	OpenWebFailed = 1 # 打开web失败
	OpenAdminPageFailed = 2 # 切换到admin界面失败
	UpdateButtonDisable = 3 # 升级按键不可点击
	SendUpdateFileFailed = 4 # 发送升级文件失败
	ProcessUpdateFileFailed = 5 # 处理升级文件失败

def updateTest(driver, ipaddr, upgradeFileFullPath):
	print("start time")
	print(time.strftime('%Y-%m-%d %H:%M:%S\n',time.localtime(time.time())))
	# 在这里修改IP地址
	driver.get('http://' + ipaddr + ':8080/update.html')
	# 直到密码框出现
	waitIdTarget( driver, 'loginPasswordField-inputEl' )

	# 登录界面
	print('login\n')
	# 输入密码
	driver.find_element( By.ID, "loginPasswordField-inputEl" ).send_keys("mpeg101")

	# 单击Login
	login = driver.find_element(By.XPATH, "//span[@data-ref='btnEl']")
	login.click()
	#ret = waitIdTarget(driver, 'tab-1109')
	#if( ret == 1 ):
	#	return Upgrade.OpenWebFailed

	## 切换到admin界面,对于impulse300D来说就是这个按键（'tab-1109'）
	#print('click Admin page')
	#driver.find_element_by_id('tab-1109').click()
	#ret = waitIdTarget(driver, 'adminUpdateButton-btnInnerEl')
	#if( ret == 1 ):
	#	return Upgrade.OpenAdminPageFailed

	## 切换到升级页面
	#print('click update page')
	#driver.find_element(By.ID, 'adminUpdateButton-btnInnerEl').click()
	#ret = waitIdTarget(driver, 'form-file-button-fileInputEl')
	#if( ret == 1 ):
	#	return Upgrade.UpdateButtonDisable
	#tempObj = driver.find_element(By.ID,'adminUpdateButton-btnInnerEl')
	#if( tempObj.is_enabled() and tempObj.is_displayed() ):
	#	print("wait for updare")
	#else:
	#	print("can't update")
	#	return Upgrade.UpdateButtonDisable
	time.sleep(3)
	print('click Update page\n')
	driver.find_element( By.XPATH, '//*[@id="tab-1030-btnInnerEl"]').click()
	time.sleep(3)

	## 切换到选择文件界面 form-file-button-fileInputEl
	print('click upgrade file\n')
	upload_element = driver.find_element(By.XPATH, '//*[@id="form-file-button-fileInputEl"]')
	time.sleep(3)

	'''
	在这里设置升级文件的名字
	'''
	## 选择升级文件
	print('select upgrade file\n')
	upload_element.send_keys( upgradeFileFullPath )
	time.sleep(2)

	sendUpgradeFileRet = 1;

	#这里最长等待约为4*10秒，等待升级文件传输完成
	for x in range(10):

		# 判断某个ID是否可见，不通版本的正常升级
		if( driver.find_element(By.XPATH, '//*[@id="messagebox-1001_header"]').is_displayed() ):
			sendUpgradeFileRet = 0
		else:
			sendUpgradeFileRet = 1

		if( sendUpgradeFileRet == 0 ):
			break
		else:
			time.sleep(4)

	# 如果上面的for循环退出的时候，sendUpgradeFileRet 这个值不为零时代表失败
	# 意味着传输升级文件失败
	if( sendUpgradeFileRet == 0 ):
		if( driver.find_element( By.XPATH, '//*[@id="messagebox-1001_header-title-textEl"]').text == "Failed to upload file"):
			print("send upgrade file failed\n")
			return Upgrade.SendUpdateFileFailed
		else:
			print("send upgrade file success\n")
	else:
		print("send upgrade file failed[unknown]\n")
		return Upgrade.SendUpdateFileFailed

	# 下面还需要判断是否可以点击-----------------------------
	# 如果提示是否升级，点击yes
	if( driver.find_element( By.XPATH, '//*[@id="messagebox-1001_header"]').is_displayed() ):
		tempObj = driver.find_element( By.XPATH, "//*[contains(text(),'Yes')][@data-ref='btnInnerEl']/..")
		if( tempObj.is_enabled() and tempObj.is_displayed() ):
			print( tempObj.get_attribute('id') )
			tempObj.click()
		else:
			return Upgrade.SendUpdateFileFailed
	elif( driver.find_element( By.XPATH, '//*[@id="updateOptionsWindow_header-title-textEl"]').is_displayed() ):
		tempObj = driver.find_element( By.XPATH, "//*[contains(text(),'Continue With Update')][@data-ref='btnInnerEl']/..")
		if( tempObj.is_enabled() and tempObj.is_displayed() ):
			print( tempObj.get_attribute('id') )
			tempObj.click()
		else:
			return Upgrade.SendUpdateFileFailed
	else: # 其他情况视为失败
		print( "send upgrade file failed\n")
		return Upgrade.SendUpdateFileFailed

	# <div class="x-component x-window-text x-box-item x-component-default" id="messagebox-1001-msg" style="margin: 0px; right: auto; left: 0px; top: 0px; width: 220px;">Update Successful</div>
	waitIdTarget(driver, 'messagebox-1001-msg')
	waitTimes = 360
	# 这个次数要根据实际的时间做一点修改，尽可能大一点
	for x in range(waitTimes):
		updateStatus = driver.find_element(  By.XPATH, '//*[@id="messagebox-1001-msg"]').text
		if( updateStatus != "" ):
			#print(updateStatus)
			if(updateStatus == "Update Successful"):
				print( "update success, rebooting\n")
				break
			elif( updateStatus == "Performing Post-Update Actions" ):
				break;
		ret = waitIdAndTextTarget( driver, "messagebox-1001_header-title-textEl", "Warning", 1)
		# 找到匹配的数据证明失败了
		if( ret == 0 ):
			return Upgrade.ProcessUpdateFileFailed
	if( x >= waitTimes-1 ):
		print( "update failed\n" )
		return Upgrade.ProcessUpdateFileFailed
	print('setp end')
	print("end time")
	print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	return Upgrade.Success
#----------------------end----------------------------