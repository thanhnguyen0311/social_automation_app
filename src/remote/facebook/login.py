from appium import webdriver
import time

from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import MaxRetryError

from src.enum.checkpoints import LoginEnum
from src.ld_manager.is_running import is_running
from src.ld_manager.quit_ld import quit_ld
from src.ld_manager.reboot_ld import reboot_ld
from src.ld_manager.run_ld import run_ld
from src.services.deviceService import check_device_exists
from src.services.fbService import update_last_login
from src.utils.findText import find_text_in_screenshot
from src.utils.imageUtils import capture_checkpoint


def login_facebook(data):
    data.device = check_device_exists(data)

    while True:
        if is_running(data.device) is False:
            run_ld(data.device)
            time.sleep(20)

        desired_cap = {
            "uuid": data.device.uuid,
            "platformName": "Android",
            "appPackage": "com.facebook.katana",
            "appActivity": "com.facebook.katana.LoginActivity"
        }

        try:
            driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
            driver.implicitly_wait(60)

            time.sleep(15)

            checkpoint = capture_checkpoint(driver, (400, 55, 600, 130))
            if LoginEnum.LOGIN_SUCCESS.value == checkpoint:
                update_last_login(data.facebook_account_id)
                print("Login successful.")
                return driver

            element = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
            element.click()

            element.send_keys(data.email.email_address)

            element = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
            element.click()

            element.send_keys(data.password)

            while find_text_in_screenshot(driver, "Forgot password"):
                element = driver.find_element_by_xpath('//android.view.View[@content-desc="Log in"]')
                element.click()
                time.sleep(10)

            pass_login_checkpoint(driver)

            checkpoint = capture_checkpoint(driver, (400, 55, 600, 130))
            if LoginEnum.LOGIN_SUCCESS.value == checkpoint:
                update_last_login(data.facebook_account_id)
                print("Login successful.")
                return driver

        except MaxRetryError:
            continue

        except WebDriverException as e:
            print(f"Error: {e}")
            quit_ld(data.device)
            continue


def pass_login_checkpoint(driver):
    while True:
        if find_text_in_screenshot(driver, "Facebook uses this"):
            element = driver.find_element_by_xpath('//android.view.ViewGroup[@content-desc="Allow"]')
            element.click()
            time.sleep(3)
            element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[2]')
            element.click()
            time.sleep(3)
            continue

        if find_text_in_screenshot(driver, "save the login"):
            element = driver.find_element_by_xpath('//android.view.View[@content-desc="Save"]')
            element.click()
            time.sleep(3)
            continue
        break
    pass
