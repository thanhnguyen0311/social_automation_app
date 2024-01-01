from appium import webdriver
import time

from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import MaxRetryError

from src.enum.checkpoints import LoginEnum
from src.ld_manager.is_running import is_running
from src.ld_manager.quit_ld import quit_ld
from src.ld_manager.run_ld import run_ld
from src.services.deviceService import check_device_exists
from src.services.fbService import update_last_login, update_account_status
from src.utils.findText import find_text_in_screenshot
from src.utils.imageUtils import capture_checkpoint


def login_facebook(data):
    # data.device = check_device_exists(data)

    while True:
        if is_running(data.device) is False:
            run_ld(data.device)
            time.sleep(20)
            if data.device.created:
                time.sleep(20)

        desired_cap = {
            "udid": data.device.uuid,
            "platformName": "Android",
            "appPackage": "com.ldmnq.launcher3",
            "appActivity": "com.android.launcher3.Launcher"
        }

        try:
            driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
            driver.implicitly_wait(30)

            driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Facebook"]').click()

            time.sleep(10)

            checkpoint = capture_checkpoint(driver, (400, 55, 600, 130))
            print(checkpoint)
            if (find_text_in_screenshot(driver, "on your mind?")
                    or LoginEnum.LOGIN_SUCCESS.value == checkpoint):
                update_last_login(data.facebook_account_id)
                print(f"Login successful to account {data.email.email_address}.")
                return driver

            pass_login_checkpoint(driver, data)

            if find_text_in_screenshot(driver, "Forgot password"):
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
                    time.sleep(15)

                pass_login_checkpoint(driver, data)

            time.sleep(2)

            checkpoint = capture_checkpoint(driver, (400, 55, 600, 130))
            if find_text_in_screenshot(driver, "on your mind?") or LoginEnum.LOGIN_SUCCESS.value == checkpoint:
                update_last_login(data.facebook_account_id)
                print(f"Login successful to account {data.email.email_address}.")
                return driver

        except MaxRetryError:
            continue

        except WebDriverException as e:
            print(f"Error: {e}")
            quit_ld(data.device)
            continue


def pass_login_checkpoint(driver, data):
    while True:

        time.sleep(3)

        if find_text_in_screenshot(driver, "Turn on contact uploading"):
            driver.find_element_by_xpath('//android.view.ViewGroup[@content-desc="Not now"]').click()

        if find_text_in_screenshot(driver, "Something went wrong"):
            driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[2]').click()

        if find_text_in_screenshot(driver, "is not visible") or find_text_in_screenshot(driver, "appeal"):
            print("check point")
            update_account_status(data.facebook_account_id, "CHECKPOINT")
            driver.quit()
            return

        if find_text_in_screenshot(driver, "Continue in English"):
            element = driver.find_element_by_xpath('//android.view.ViewGroup[@content-desc="Continue in English (US)"]')
            element.click()
            continue

        if find_text_in_screenshot(driver, "Add email"):
            element = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[3]')
            element.click()
            continue

        if find_text_in_screenshot(driver, "Add number"):
            element = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[3]')
            element.click()
            continue

        if find_text_in_screenshot(driver, "Access to contacts"):
            element = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup')
            element.click()
            continue

        if find_text_in_screenshot(driver, "Facebook uses this"):
            element = driver.find_element_by_xpath('//android.view.ViewGroup[@content-desc="Allow"]')
            element.click()
            element = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[2]')
            element.click()
            continue

        if find_text_in_screenshot(driver, "save the login"):
            element = driver.find_element_by_xpath('//android.view.View[@content-desc="Save"]')
            element.click()
            continue

        break
