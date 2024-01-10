import time

from selenium.common.exceptions import WebDriverException

from src.ld_manager.adb_shells import open_link
from src.remote.facebook.login import LoginFacebook


class LikePostFB(LoginFacebook):
    def __init__(self, data, link):
        self.link = link
        super().__init__(data)

    def __run__(self):
        self.driver = super().__run__()
        open_link(link=self.link, device=self.data.device)
        time.sleep(5)
        try:
            element = self.driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector('
                ').description("Like button. Double tap and hold to react."));')

            time.sleep(3)

            super().__find_element__(
                xpath='//android.view.ViewGroup[@content-desc="Like button. Double tap and hold to react."]').click()

            print(f"Liked : {self.link}")

        except WebDriverException as e:
            print(e)
            return
