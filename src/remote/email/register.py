import random
import time

from appium import webdriver
from selenium.common.exceptions import WebDriverException

from src.enum.EmailEnum import EmailEnum
from src.ld_manager.adb_shells import input_text_device
from src.remote.driver import Driver
from src.services.emailService import update_email_status
from src.utils.findText import get_email_type, find_text_in_screenshot
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError


class RegisterEmail(Driver):
    def __init__(self, data):
        super().__init__(data)

    def __run__(self):
        if "hotmail.com" in self.data.email_address:
            self.register_hotmail()

    def register_hotmail(self):
        self.driver = super().__run__()

        super().__find_element__(xpath='//android.widget.TextView[@content-desc="Aqua Mail"]').click()

        time.sleep(3)
        if find_text_in_screenshot(self.driver, "Your universal email app"):
            self.driver.find_element(By.XPATH,
                                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                '.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view'
                                '.ViewGroup/android.view.View').click()

        time.sleep(3)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(66)

        self.driver.find_element(By.XPATH,
                            '//android.view.View[@content-desc="Create a Microsoft account"]/android.widget.TextView').click()

        time.sleep(8)
        input_text_device(self.data.email_address, self.data.device)

        check = True

        while True:
            time.sleep(2)
            if check:
                self.driver.press_keycode(61)
                time.sleep(1)
            self.driver.press_keycode(61)
            time.sleep(1)
            self.driver.press_keycode(61)
            time.sleep(1)
            self.driver.press_keycode(61)
            time.sleep(1)
            self.driver.press_keycode(61)
            time.sleep(1)
            self.driver.press_keycode(66)

            time.sleep(3)
            if find_text_in_screenshot(self.driver, "Introduction to the"):
                self.driver.press_keycode(66)
                check = not check
                continue
            else:
                break

        time.sleep(5)
        input_text_device(self.data.password, self.data.device)
        time.sleep(10)

        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(66)

        time.sleep(5)
        input_text_device(self.data.first_name, self.data.device)

        time.sleep(1)
        self.driver.press_keycode(61)

        time.sleep(3)
        input_text_device(self.data.last_name, self.data.device)

        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(66)

        time.sleep(3)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(66)

        self.driver.find_element(By.XPATH,
                            f'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.CheckedTextView[{str(random.randint(2, 8))}]').click()

        time.sleep(3)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(66)

        self.driver.find_element(By.XPATH,
                            f'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.CheckedTextView[{str(random.randint(2, 9))}]').click()

        time.sleep(3)
        self.driver.press_keycode(61)
        time.sleep(1)
        input_text_device(str(random.randint(1989, 2002)), self.data.device)

        time.sleep(3)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(66)

        print("CHECKPOINT")
        while True:
            if find_text_in_screenshot(self.driver, "Let this app access your"):
                print(f"Successfully created {self.data.email_address}")
                update_email_status(self.data.email_id, "ALIVE")
                break

        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(61)
        time.sleep(1)
        self.driver.press_keycode(66)
        time.sleep(3)

        return
