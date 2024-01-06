import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from src.remote.facebook.login import LoginFacebook
from src.utils.findText import find_text_in_screenshot
from src.utils.randomGenerate import generate_random_true25percent


class FarmNewFeed(LoginFacebook):
    def __init__(self, data):
        super().__init__(data)

    def __run__(self):
        self.driver = super().__run__()
        i = 1
        while True:
            try:
                i = i + 1
                element = self.driver.find_element_by_android_uiautomator(
                    'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector('
                    ').description("Like button. Double tap and hold to react."));')

                time.sleep(5)

                if generate_random_true25percent():
                    super().__find_element__(
                        xpath='//android.view.ViewGroup[@content-desc="Like button. Double tap and hold to react."]').click()

                    time.sleep(5)

                element = self.driver.find_element_by_android_uiautomator(
                    'new UiScrollable(new UiSelector().scrollable('
                    'true).instance(0)).scrollToEnd(1);')

                time.sleep(5)
                if int(i) == 50:
                    self.driver.quit()
                    return

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
                    continue
