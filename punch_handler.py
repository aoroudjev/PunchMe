import sys
import time
from datetime import datetime

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def start_driver() -> webdriver:
    options = Options()
    options.add_argument("--headless=new")
    options.EnableVerboseLogging = False
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        print('Webdriver start failed:', e)
        return None


def sleep_until(hour, minute):
    t = datetime.today()
    future = datetime(t.year, t.month, t.day, int(hour), int(minute))
    if t.timestamp() > future.timestamp():
        sys.exit()
    time.sleep((future - t).total_seconds())


def login(driver, credentials):
    driver.get('https://portalapps.insperity.com/QuickPunch/')
    input_elements = [elem for elem in driver.find_elements(By.TAG_NAME, 'input') if
                      elem.accessible_name in credentials]
    for i in input_elements:
        i.send_keys(credentials[str(i.accessible_name)])
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    if driver.title != 'Quick Punch':
        raise EOFError("Can't login")


def clock(driver, button_name, credentials):
    login(driver, credentials)
    clocking_buttons = driver.find_elements(By.TAG_NAME, 'button')
    for button in clocking_buttons:
        if button.accessible_name == button_name:
            # Comment until ready for deployment
            # button.click()
            time.sleep(5)
