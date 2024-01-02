import time

from appium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError

from src.utils.imageUtils import capture_checkpoint


def register_email():
    desired_cap = {
        "udid": "emulator-5554",
        "platformName": "Android",
        "appPackage": "com.android.settings",
        "appActivity": "com.android.settings/.Settings"
    }

    while True:
        try:
            driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
            driver.implicitly_wait(30)
            return driver

        except MaxRetryError:
            continue

        except WebDriverException as e:
            print(f"Error: {e}")
            continue


register_email()
