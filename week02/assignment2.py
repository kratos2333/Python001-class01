from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException

try:
    # Open shimo website
    chrome_browser = webdriver.Chrome()
    chrome_browser.get("https://shimo.im/welcome")
    time.sleep(1)

    # find the login button by class and click
    login_btn = chrome_browser.find_element_by_xpath('//button[@class="login-button btn_hover_style_8"]')
    login_btn.click()
    time.sleep(1)

    # find the userName textbox
    chrome_browser.find_element_by_xpath('//input[@type="text"]').send_keys('dummy@dummy.com')
    chrome_browser.find_element_by_xpath('//input[@type="password"]').send_keys('dummyPassword')
    time.sleep(1)

    # find the submit button and click
    submit_btn = chrome_browser.find_element_by_xpath('//button[contains(@class,"sm-button submit")]')
    submit_btn.click()

except NoSuchElementException as nse:
    print("Please double check the following xpath.")
    print(nse)

finally:
    chrome_browser.close()
