import random
import time

from appium import webdriver
from selenium.common.exceptions import WebDriverException

from src.enum.EmailEnum import EmailEnum
from src.ld_manager.adb_shells import input_text_device
from src.services.emailService import update_email_status
from src.utils.findText import get_email_type, find_text_in_screenshot
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError


def register_email(data):
    desired_cap = {
        "udid": data.device.uuid,
        "platformName": "Android",
        "appPackage": "com.ldmnq.launcher3",
        "appActivity": "com.android.launcher3.Launcher"
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
    input_text_device(data.email_address, data.device)

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
    input_text_device(data.password, data.device)
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
    input_text_device(data.first_name, data.device)

    time.sleep(1)
    driver.press_keycode(61)

    time.sleep(3)
    input_text_device(data.last_name, data.device)

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
    input_text_device(str(random.randint(1989, 2002)), data.device)

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
