from appium import webdriver
from selenium.webdriver.common.by import By

from src.ld_manager.quit_ld import quit_ld
from src.remote.setup import driver
from src.utils.findText import find_text_in_screenshot


class Driver:
    def __init__(self, data):
        self.data = data
        self.is_running = True
        self.driver = webdriver
        self.desired_cap = {
            "udid": data.device.uuid,
            "platformName": "Android",
            "appPackage": "com.ldmnq.launcher3",
            "appActivity": "com.android.launcher3.Launcher"
        }

    def __run__(self):
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.desired_cap)
        self.driver.implicitly_wait(30)
        return self.driver

    def __find_element__(self, xpath=None):
        if not self.is_running:
            self.__quit__()

        if find_text_in_screenshot(self.driver, "System UI isn't responding"):
            driver.find_element(By.XPATH,
                                '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button[1]').click()
            self.__run__()

        if xpath is not None:
            element = self.driver.find_element(By.XPATH, xpath)
            return element

    def __stop__(self):
        self.is_running = False

    def __quit__(self):
        self.driver.quit()
        quit_ld(self.data.device)
        self.data.device.is_running = False
