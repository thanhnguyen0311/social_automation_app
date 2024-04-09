import random
import time

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import TouchActions
from selenium.webdriver.common.by import By

from src.constants.constants import COMMENTS, LAMNGOCTHANH_PAGEID, LNT_COMMENTS, HCSPA_COMMENTS, HCSPA_PAGEID
from src.ld_manager.adb_shells import open_link
from src.remote.facebook.login import LoginFacebook
from src.utils.findText import find_text_in_screenshot


class LikePostFB(LoginFacebook):
    def __init__(self, data, link):
        self.link = link
        super().__init__(data)

    def __run__(self):
        self.driver = super().__run__()
        time.sleep(4)
        for post_id in self.link:
            array = post_id.split("_")
            open_link(link=f'https://m.facebook.com/{array[1]}', device=self.data.device)
            time.sleep(3)
            if find_text_in_screenshot(self.driver, "Open with"):
                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                         '.widget.FrameLayout/android.widget.ScrollView/android.widget.ListView'
                                         '/android.widget.LinearLayout[1]/android.widget.LinearLayout').click()
                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                         '.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout'
                                         '/android.widget.Button[2]').click()
                time.sleep(5)

            try:
                screen_size = self.driver.get_window_size()

                # Define start and end coordinates for the swipe
                start_x = screen_size['width'] // 2
                start_y = screen_size['height'] // 2
                end_x = start_x
                end_y = screen_size['height'] * 0.2  # Adjust this value if needed for precise scrolling

                scroll_count = 5
                # Perform the scrolling action using TouchAction
                if array[0] == HCSPA_PAGEID:
                    for _ in range(scroll_count):
                        self.driver.swipe(start_x, start_y, end_x, end_y, duration=500)
                        time.sleep(1)

                element = self.driver.find_element_by_android_uiautomator(
                    'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().description("Like button. Double tap and hold to react."));')
                time.sleep(3)

                self.driver.find_element(By.XPATH,
                                         '(//android.view.ViewGroup[@content-desc="Like button. Double tap and hold to react."])[1]').click()
                time.sleep(3)
                print(f"Liked : {self.link}")
                if random.random() < 0.05:
                    list_comments = []
                    if array[0] == LAMNGOCTHANH_PAGEID:
                        list_comments = COMMENTS + LNT_COMMENTS
                    elif array[0] == HCSPA_PAGEID:
                        list_comments = COMMENTS + HCSPA_COMMENTS

                    element = self.driver.find_element(By.XPATH,
                                                       '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
                    element.click()
                    element.send_keys(random.choice(list_comments))
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, '//android.view.ViewGroup[@content-desc="Send"]').click()
                    time.sleep(2)



            except WebDriverException as e:
                super().__stop__()
                return

        super().__stop__()
        return
