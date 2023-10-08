import sys
import time
from datetime import datetime

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def start_driver() -> webdriver:
    options = Options()
    options.add_argument('--headless')
    options.EnableVerboseLogging = False
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        print('Webdriver start failed:', e)
        return None


def sleep_until(hour, minute):
    print(f'waiting until {hour}:{minute}...')
    t = datetime.today()
    future = datetime(t.year, t.month, t.day, hour, minute)
    if t.timestamp() > future.timestamp():
        print("That time already passed")
        sys.exit()
    time.sleep((future - t).total_seconds())


def login(driver, credentials):
    driver.get('https://portalapps.insperity.com/QuickPunch/')
    print("Logging in...")
    input_elements = [elem for elem in driver.find_elements(By.TAG_NAME, 'input') if
                      elem.accessible_name in credentials]
    for i in input_elements:
        i.send_keys(credentials[str(i.accessible_name)])
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    if driver.title == 'Quick Punch':
        print('Logged in successfully')
    else:
        raise EOFError("Can't login")


def clock(driver, button_name):
    # Clock in or out depending on passed button option and log out
    time.sleep(3)
    clocking_buttons = driver.find_elements(By.TAG_NAME, 'button')
    print("Clocking operation...")
    for button in clocking_buttons:
        if button.accessible_name == button_name:
            button.click()
            print('Clock operation successful')
    time.sleep(3)
