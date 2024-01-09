# sync 同步
from playwright.sync_api import sync_playwright

# p = sync_playwright().start()
# 使用with不需要调用 start() 和 stop()
with sync_playwright() as p:
    # headless缺省为true，不显示图形界面
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    input('2')
    page.goto('https://10.200.1.73/login')
    input('2')
    page.locator('[name="username"]').fill('admin')
    page.locator('[name="password"]').fill('wellav123')
    input('1')
    browser.close()