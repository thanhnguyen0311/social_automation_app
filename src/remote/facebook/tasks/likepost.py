import random
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from src.constants.constants import COMMENTS
from src.ld_manager.adb_shells import open_link
from src.remote.facebook.login import LoginFacebook
from src.utils.findText import find_text_in_screenshot


class LikePostFB(LoginFacebook):
    def __init__(self, data, link):
        self.link = link
        super().__init__(data)

    def __run__(self):
        self.driver = super().__run__()
        time.sleep(5)
        for post_id in self.link:
            open_link(link=f'https://www.facebook.com/{post_id}', device=self.data.device)
            time.sleep(5)
            if find_text_in_screenshot(self.driver, "Open with"):
                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.LinearLayout').click()
                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.Button[2]').click()
                time.sleep(5)

            try:
                element = self.driver.find_element_by_android_uiautomator(
                    'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector('
                    ').description("Like button. Double tap and hold to react."));')

                time.sleep(3)

                self.driver.find_element(By.XPATH,
                                         '(//android.view.ViewGroup[@content-desc="Like button. Double tap and hold to react."])[1]').click()
                time.sleep(3)
                print(f"Liked : {self.link}")
                if random.random() < 0.05:
                    LNT_COMMENT = ['còn ko ạ', 'gi']
                    element = self.driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
                    element.click()
                    element.send_keys(random.choice(COMMENTS))
                    time.sleep(1)
                    self.driver.find_element(By.XPATH,'//android.view.ViewGroup[@content-desc="Send"]').click()



            except WebDriverException as e:
                super().__stop__()
                return

        super().__stop__()
        return
