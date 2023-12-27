from appium import webdriver
import time

from selenium.common.exceptions import WebDriverException

from src.enum.checkpoints import LoginEnum
from src.ld_manager.is_running import is_running
from src.ld_manager.reboot_ld import reboot_ld
from src.ld_manager.run_ld import run_ld
from src.services.deviceService import check_device_exists
from src.services.fbService import update_last_login
from src.utils.imageUtils import capture_checkpoint


def login_facebook(data):
    data.device = check_device_exists(data)
    if is_running(data.device) is False:
        run_ld(data.device)

    while True:
        time.sleep(15)

        desired_cap = {
            "uuid": data.device.uuid,
            "platformName": "Android",
            "appPackage": "com.ldmnq.launcher3",
            "appActivity": "com.android.launcher3.Launcher"
        }

        try:
            driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
            driver.implicitly_wait(30)

            element = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Facebook"]')
            element.click()

            time.sleep(5)

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

            checkpoint = capture_checkpoint(driver, (200, 700, 520, 930))
            while LoginEnum.LOGIN_BUTTON.value == checkpoint:
                element = driver.find_element_by_xpath('//android.view.View[@content-desc="Log in"]')
                element.click()
                time.sleep(1)
                checkpoint = capture_checkpoint(driver, (200, 700, 520, 930))

            checkpoint = capture_checkpoint(driver, (200, 55, 520, 130))
            while LoginEnum.WAIT_LOGIN.value == checkpoint:
                checkpoint = capture_checkpoint(driver, (200, 55, 520, 130))
                time.sleep(1)

            checkpoint = capture_checkpoint(driver, (200, 55, 520, 130))
            if LoginEnum.ACCESS_TO_CONTACT.value == checkpoint:
                reboot_ld(data.device)
                continue

            element = driver.find_element_by_xpath(
                    '//android.view.ViewGroup[@content-desc="Allow"]')
            element.click()

            element = driver.find_element_by_xpath(
                    '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[2]')
            element.click()

            element = driver.find_element_by_xpath(
                    '//android.widget.Button[@content-desc="Save"]/android.view.ViewGroup')
            element.click()

            if LoginEnum.LOGIN_SUCCESS == checkpoint:
                update_last_login(data.facebook_account_id)
                print("Login successful.")
                return driver

            else:
                print("Login Failed.")
                return False

        except WebDriverException:
            reboot_ld(data.device)
            continue
