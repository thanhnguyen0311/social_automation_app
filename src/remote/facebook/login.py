from appium import webdriver
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError

from src.enum.checkpoints import LoginEnum
from src.services.fbService import update_last_login, update_account_status, get_2fa_code
from src.utils.findText import find_text_in_screenshot
from src.utils.imageUtils import capture_checkpoint


def login_facebook(data):
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

            # if not find_package_running("com.facebook.katana", data.device):
            driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="Facebook"]').click()

            time.sleep(10)

            checkpoint = capture_checkpoint(driver, (400, 55, 600, 130))
            if (find_text_in_screenshot(driver, "on your mind?")
                    or LoginEnum.LOGIN_SUCCESS.value == checkpoint or LoginEnum.LOGIN_SUCCESS2.value == checkpoint):
                update_last_login(data.facebook_account_id)
                print(f"Login successful to account {data.email.email_address}.")
                return driver

            pass_login_checkpoint(driver, data)
            if data.status == "CHECKPOINT":
                driver.quit()
                return

            if find_text_in_screenshot(driver, "Forgot password"):
                element = driver.find_element(By.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
                element.click()

                element.send_keys(data.email.email_address)

                element = driver.find_element(By.XPATH,
                                              '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
                element.click()
                element.send_keys(data.password)

                while find_text_in_screenshot(driver, "Forgot password"):
                    element = driver.find_element(By.XPATH, '//android.view.View[@content-desc="Log in"]')
                    element.click()
                    time.sleep(15)

                pass_login_checkpoint(driver, data)
                if data.status == "CHECKPOINT":
                    driver.quit()
                    return

            time.sleep(2)

            checkpoint = capture_checkpoint(driver, (400, 55, 600, 130))
            if (find_text_in_screenshot(driver, "on your mind?")
                    or LoginEnum.LOGIN_SUCCESS.value == checkpoint):
                update_last_login(data.facebook_account_id)
                print(f"Login successful to account {data.email.email_address}.")
                return driver

        except MaxRetryError:
            continue

        except WebDriverException as e:
            print(f"Error: {e}")
            continue

        except Exception as e:
            time.sleep(10)
            continue


def pass_login_checkpoint(driver, data):
    while True:
        time.sleep(3)
        if (find_text_in_screenshot(driver, "Check your notifications") or
                find_text_in_screenshot(driver, "Waiting for approval")):
            driver.find_element(By.XPATH, '//android.view.View[@content-desc="Try another way"]').click()
            driver.find_element(By.XPATH,
                                '//android.widget.RadioButton[@content-desc="Authentication app, Get a code from the app you set up."]').click()
            driver.find_element(By.XPATH,
                                '//android.widget.Button[@content-desc="Continue"]/android.view.ViewGroup').click()
            element = driver.find_element(By.XPATH,
                                          '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
            element.click()
            element.send_keys(get_2fa_code(data.auth_2fa))

            driver.find_element(By.XPATH,
                                '//android.widget.Button[@content-desc="Continue"]/android.view.ViewGroup').click()
            continue

        if (find_text_in_screenshot(driver, "Turn on contact uploading")
                or find_text_in_screenshot(driver, "See who's on")):
            driver.find_element(By.XPATH, '//android.view.ViewGroup[@content-desc="Not now"]').click()
            continue

        if find_text_in_screenshot(driver, "Something went wrong"):
            driver.find_element(By.XPATH,
                                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[2]').click()
            continue

        if find_text_in_screenshot(driver, "Are you sure want to skip"):
            driver.find_element(By.XPATH,
                                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.Button[1]').click()
            continue

        if find_text_in_screenshot(driver, "We couldn't find any"):
            driver.find_element(By.XPATH, '//android.view.ViewGroup[@content-desc="Next"]').click()
            continue

        if find_text_in_screenshot(driver, "is not visible") or find_text_in_screenshot(driver, "appeal"):
            print("check point")
            data.status = "CHECKPOINT"
            update_account_status(data.facebook_account_id, "CHECKPOINT")
            driver.quit()
            return

        if find_text_in_screenshot(driver, "Continue in English"):
            element = driver.find_element(By.XPATH,
                                          '//android.view.ViewGroup[@content-desc="Continue in English (US)"]')
            element.click()
            continue

        if find_text_in_screenshot(driver, "Add email"):
            element = driver.find_element(By.XPATH,
                                          '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[3]')
            element.click()
            continue

        if find_text_in_screenshot(driver, "Add number"):
            element = driver.find_element(By.XPATH,
                                          '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[3]')
            element.click()
            continue

        if find_text_in_screenshot(driver, "Access to contacts"):
            element = driver.find_element(By.XPATH,
                                          '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup')
            element.click()
            continue

        if find_text_in_screenshot(driver, "Facebook uses this"):
            element = driver.find_element(By.XPATH, '//android.view.ViewGroup[@content-desc="Allow"]')
            element.click()
            element = driver.find_element(By.XPATH,
                                          '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[2]')
            element.click()
            continue

        if find_text_in_screenshot(driver, "save the login"):
            element = driver.find_element(By.XPATH, '//android.view.View[@content-desc="Save"]')
            element.click()
            continue

        break

# desired_cap = {
#         "udid": "emulator-5572",
#         "platformName": "Android",
#         "appPackage": "com.ldmnq.launcher3",
#         "appActivity": "com.android.launcher3.Launcher"
#     }
#
# driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
# driver.implicitly_wait(30)
#
# # if not find_package_running("com.facebook.katana", data.device):
# driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="Facebook"]').click()
#
# element = driver.find_element(By.XPATH,
#                               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
# element.click()
#
# subprocess.run([LDCONSOLE_PATH] + ["action", "--name", "LDPlayer-9", "--key", "call.input", "--value", "Y4gRUSu6g341Q4k"])