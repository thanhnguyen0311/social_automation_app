import random
import time

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains

from src.enum.EmailEnum import EmailEnum
from src.services.emailService import update_email_status
from src.utils.findText import get_email_type, find_text_in_screenshot
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError

from src.utils.textToKeyCode import text_to_keycodes


def register_email(data):
    print(data.email_address)
    if data.device.created:
        time.sleep(15)

    proxy_address = '202.159.35.153'
    proxy_port = '443'
    desired_cap = {
        "udid": data.device.uuid,
        "platformName": "Android",
        "appPackage": "com.ldmnq.launcher3",
        "appActivity": "com.android.launcher3.Launcher"
        # 'proxy': {
        #     'httpProxy': f"{proxy_address}:{proxy_port}",
        #     'ftpProxy': f"{proxy_address}:{proxy_port}",
        #     'sslProxy': f"{proxy_address}:{proxy_port}",
        #     'proxyType': 'MANUAL',
        # }
    }



    while True:
        try:
            driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
            driver.implicitly_wait(30)

            if get_email_type(data.email_address) == EmailEnum.GMAIL.value:
                register_gmail(driver=driver, data=data)
            if get_email_type(data.email_address) == EmailEnum.HOTMAIL.value:
                register_hotmail(driver=driver, data=data)

            return driver

        except MaxRetryError:
            continue

        except WebDriverException as e:
            print(f"Error: {e}")
            continue


def register_gmail(driver, data):
    return


def register_hotmail(driver, data):
    driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="Aqua Mail"]').click()

    time.sleep(3)
    if find_text_in_screenshot(driver, "Your universal email app"):
        driver.find_element(By.XPATH,
                            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.View').click()

    time.sleep(3)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(66)

    driver.find_element(By.XPATH,
                        '//android.view.View[@content-desc="Create a Microsoft account"]/android.widget.TextView').click()

    time.sleep(8)
    text_to_keycodes(data.email_address, driver)

    check = True

    while True:
        time.sleep(2)
        if check:
            driver.press_keycode(61)
            time.sleep(1)
        driver.press_keycode(61)
        time.sleep(1)
        driver.press_keycode(61)
        time.sleep(1)
        driver.press_keycode(61)
        time.sleep(1)
        driver.press_keycode(61)
        time.sleep(1)
        driver.press_keycode(66)

        time.sleep(3)
        if find_text_in_screenshot(driver, "Introduction to the"):
            driver.press_keycode(66)
            check = not check
            continue
        else:
            break

    time.sleep(5)
    text_to_keycodes(data.password, driver)
    time.sleep(10)

    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(66)

    time.sleep(5)
    text_to_keycodes(data.first_name, driver)

    time.sleep(1)
    driver.press_keycode(61)

    time.sleep(3)
    text_to_keycodes(data.last_name, driver)

    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(66)

    time.sleep(3)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(66)

    driver.find_element(By.XPATH,
                        f'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.CheckedTextView[{str(random.randint(2, 8))}]').click()

    time.sleep(3)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(66)

    driver.find_element(By.XPATH,
                        f'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.CheckedTextView[{str(random.randint(2, 9))}]').click()

    time.sleep(3)
    driver.press_keycode(61)
    time.sleep(1)
    text_to_keycodes(str(random.randint(1989, 2002)), driver)

    time.sleep(3)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(66)

    print("CHECKPOINT")
    while True:
        if find_text_in_screenshot(driver, "Let this app access your"):
            print(f"Successfully created {data.email_address}")
            update_email_status(data.email_id, "ALIVE")
            break

    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(61)
    time.sleep(1)
    driver.press_keycode(66)
    time.sleep(3)

    return
