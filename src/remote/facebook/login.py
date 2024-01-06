import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError

from src.enum.checkpoints import LoginEnum
from src.remote.driver import Driver
from src.services.fbService import update_last_login, update_account_status, get_2fa_code
from src.utils.findText import find_text_in_screenshot
from src.utils.imageUtils import capture_checkpoint


class LoginFacebook(Driver):
    def __init__(self, data):
        super().__init__(data)

    def __run__(self):
        while True:
            try:
                self.driver = super().__run__()
                super().__find_element__(xpath='//android.widget.TextView[@content-desc="Facebook"]').click()

                time.sleep(10)

                checkpoint = capture_checkpoint(self.driver, (400, 55, 600, 130))
                if (find_text_in_screenshot(self.driver, "on your mind?")
                        or LoginEnum.LOGIN_SUCCESS.value == checkpoint or LoginEnum.LOGIN_SUCCESS2.value == checkpoint):
                    update_last_login(self.data.facebook_account_id)
                    print(f"Login successful to account {self.data.email.email_address}.")
                    return self.driver

                self.pass_login_checkpoint()
                if self.data.status == "CHECKPOINT":
                    self.driver.quit()
                    return

                if find_text_in_screenshot(self.driver, "Forgot password"):
                    element = super().__find_element__(
                        xpath='/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
                    element.click()

                    element.send_keys(self.data.email.email_address)

                    element = self.driver.find_element(By.XPATH,
                                                       '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
                    element.click()
                    element.send_keys(self.data.password)

                    while find_text_in_screenshot(self.driver, "Forgot password"):
                        super().__find_element__(xpath='//android.view.View[@content-desc="Log in"]').click()
                        time.sleep(15)

                    self.pass_login_checkpoint()
                    if self.data.status == "CHECKPOINT":
                        self.driver.quit()
                        return

                time.sleep(2)

                checkpoint = capture_checkpoint(self.driver, (400, 55, 600, 130))
                if (find_text_in_screenshot(self.driver, "on your mind?")
                        or LoginEnum.LOGIN_SUCCESS.value == checkpoint):
                    update_last_login(self.data.facebook_account_id)
                    print(f"Login successful to account {self.data.email.email_address}.")
                    return self.driver

            except MaxRetryError:
                continue

            except WebDriverException as e:
                if not self.is_running:
                    super().__quit__()
                    return
                print(f"Error: {e}")
                continue

            except Exception as e:
                if not self.is_running:
                    super().__quit__()
                    return
                time.sleep(10)
                continue

    def pass_login_checkpoint(self):
        while True:
            if not self.is_running:
                return None
            time.sleep(3)
            if (find_text_in_screenshot(self.driver, "Check your notifications") or
                    find_text_in_screenshot(self.driver, "Waiting for approval")):
                super().__find_element__(xpath='//android.view.View[@content-desc="Try another way"]').click()
                super().__find_element__(xpath=
                                         '//android.widget.RadioButton[@content-desc="Authentication app, Get a code from the app you set up."]').click()
                super().__find_element__(xpath=
                                         '//android.widget.Button[@content-desc="Continue"]/android.view.ViewGroup').click()
                element = super().__find_element__(xpath=
                                                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
                element.click()
                element.send_keys(get_2fa_code(self.data.auth_2fa))

                super().__find_element__(xpath=
                                         '//android.widget.Button[@content-desc="Continue"]/android.view.ViewGroup').click()
                continue

            if (find_text_in_screenshot(self.driver, "Turn on contact uploading")
                    or find_text_in_screenshot(self.driver, "See who's on")):
                super().__find_element__(xpath= '//android.view.ViewGroup[@content-desc="Not now"]').click()
                continue

            if find_text_in_screenshot(self.driver, "Something went wrong"):
                super().__find_element__(xpath=
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[2]').click()
                continue

            if find_text_in_screenshot(self.driver, "Are you sure want to skip"):
                super().__find_element__(xpath=
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.Button[1]').click()
                continue

            if find_text_in_screenshot(self.driver, "We couldn't find any"):
                super().__find_element__(xpath= '//android.view.ViewGroup[@content-desc="Next"]').click()
                continue

            if find_text_in_screenshot(self.driver, "is not visible") or find_text_in_screenshot(self.driver, "appeal"):
                print("check point")
                self.data.status = "CHECKPOINT"
                update_account_status(self.data.facebook_account_id, "CHECKPOINT")
                self.driver.quit()
                return

            if find_text_in_screenshot(self.driver, "Continue in English"):
                super().__find_element__(xpath=
                                                   '//android.view.ViewGroup[@content-desc="Continue in English (US)"]').click()
                continue

            if find_text_in_screenshot(self.driver, "Add email"):
                super().__find_element__(xpath=
                                                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[3]').click()
                continue

            if find_text_in_screenshot(self.driver, "Add number"):
                super().__find_element__(xpath='/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[3]').click()
                continue

            if find_text_in_screenshot(self.driver, "Access to contacts"):
                super().__find_element__(xpath=
                                                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup').click()
                continue

            if find_text_in_screenshot(self.driver, "Facebook uses this"):
                super().__find_element__(xpath= '//android.view.ViewGroup[@content-desc="Allow"]').click()
                super().__find_element__(xpath=
                                                   '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[2]').click()
                continue

            if find_text_in_screenshot(self.driver, "save the login"):
                super().__find_element__(xpath= '//android.view.View[@content-desc="Save"]').click()
                continue

            break
