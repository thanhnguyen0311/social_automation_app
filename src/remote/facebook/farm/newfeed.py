import time

from selenium.common.exceptions import WebDriverException
from appium.webdriver.common.touch_action import TouchAction

from src.remote.facebook.login import login_facebook
from src.utils.randomGenerate import generate_random_true25percent


def farm_newFeed(account):

    driver = login_facebook(account)
    while True:
        element = driver.find_element_by_android_uiautomator(
                'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().description("Like button. Double tap and hold to react."));')

        time.sleep(2)

        if generate_random_true25percent():
            driver.find_element_by_xpath(
                        '//android.view.ViewGroup[@content-desc="Like button. Double tap and hold to react."]').click()

            time.sleep(2)

            element = driver.find_element_by_android_uiautomator(
                    'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollToEnd(1);')