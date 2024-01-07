import random
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from src.ld_manager.adb_shells import input_text_device
from src.remote.driver import Driver
from src.services.fbService import update_account_status
from src.utils.findText import find_text_in_screenshot
from src.utils.imageUtils import capture_checkpoint


class RegisterFacebook(Driver):
    def __init__(self, data):
        super().__init__(data)

    def __run__(self):
        try:
            self.driver = super().__run__()
            super().__find_element__(xpath='//android.widget.TextView[@content-desc="Facebook"]').click()
            time.sleep(10)

            super().__find_element__(
                xpath='//android.widget.Button[@content-desc="Create new account"]/android.view.ViewGroup').click()

            super().__find_element__(xpath=
                                     '//android.widget.Button[@content-desc="Get started"]/android.view.ViewGroup').click()

            element = super().__find_element__(xpath=
                                               "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText")
            element.click()
            element.send_keys(self.data.first_name)

            element = super().__find_element__(xpath=
                                               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
            element.click()
            element.send_keys(self.data.last_name)

            super().__find_element__(
                xpath='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()

            super().__find_element__(
                xpath='/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.Button[1]').click()
            time.sleep(1)
            super().__find_element__(xpath=
                                      '//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
            time.sleep(1)
            super().__find_element__(xpath=
                                      '//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
            time.sleep(3)
            input_text_device(random.randint(20, 35), self.data.device)
            super().__find_element__(xpath=
                                      '//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()
            super().__find_element__(xpath=
                                      '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.Button[1]').click()

            super().__find_element__(xpath=
                                      '//android.widget.Button[@content-desc="Male"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView').click()
            super().__find_element__(xpath=
                                      '//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()

            super().__find_element__(xpath=
                                      '//android.widget.Button[@content-desc="Sign up with email"]/android.view.ViewGroup').click()

            element = super().__find_element__(xpath="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText")
            element.click()
            element.send_keys(self.data.email.email_address)
            super().__find_element__(xpath='//android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()

            element = super().__find_element__(xpath="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText")
            element.click()
            element.send_keys(self.data.password)
            super().__find_element__(xpath='/android.widget.Button[@content-desc="Next"]/android.view.ViewGroup').click()

            super().__find_element__(xpath='//android.widget.Button[@content-desc="Save"]/android.view.ViewGroup').click()

            super().__find_element__(xpath='//android.widget.Button[@content-desc="I agree"]/android.view.ViewGroup').click()
            time.sleep(60)

            if find_text_in_screenshot(self.driver, 'We need more information'):
                super().__find_element__(xpath='//android.view.ViewGroup[@content-desc="Continue"]').click()
                time.sleep(15)

                if find_text_in_screenshot(self.driver, "Help us confirm it's you"):
                    checkpoint = capture_checkpoint(self.driver, (70, 240, 380, 280))
                    print(checkpoint)
                    ## SOLVE CAPTCHA
                    super().__find_element__(xpath='//android.view.ViewGroup[@content-desc="Continue"]').click()

                    element = super().__find_element__(xpath='/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.EditText')
                    element.click()
                    element.send_keys(self.data.email.email_address)
                    super().__find_element__(xpath='//android.view.ViewGroup[@content-desc="Send login code"]').click()
                    ## SOLVE EMAIL CODE

                    super().__find_element__(xpath='//android.view.ViewGroup[@content-desc="Next"]').click()
                    super().__find_element__(xpath='//android.view.ViewGroup[@content-desc="Appeal"]').click()
                    ##SOLVE PHONE CODE
                    time.sleep(15)
                    super().__find_element__(xpath='//android.view.ViewGroup[@content-desc="Send by SMS"]').click()
                    time.sleep(15)
                    super().__find_element__(xpath='//android.view.ViewGroup[@content-desc="Continue"]').click()
                    time.sleep(15)

                    if find_text_in_screenshot(self.driver, "You're back on Facebook"):
                        super().__find_element__(xpath='//android.view.ViewGroup[@content-desc="Back to Facebook"]').click()
                        update_account_status(self.data.facebook_account_id, "ALIVE")

        except WebDriverException as e:
            if not self.is_running:
                return
            if find_text_in_screenshot(self.driver, "System UI"):
                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout'
                                         '/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                         '.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout'
                                         '/android.widget.Button[1]').click()
                self.__run__()
