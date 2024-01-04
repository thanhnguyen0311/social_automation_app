import threading
import time

from src.ld_manager.run_ld import run_list_ld
from src.remote.facebook.login import login_facebook
from src.utils.randomGenerate import generate_random_true25percent


def on_click_new_feed_button(list_account):
    list_account = run_list_ld(list_account)
    for account in list_account:
        account.thread = threading.Thread(target=farm_newFeed, args=(account,))
        account.thread.start()
        time.sleep(3)


def farm_newFeed(account):
    driver = login_facebook(account)
    while True:
        element = driver.find_element_by_android_uiautomator(
            'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector('
            ').description("Like button. Double tap and hold to react."));')

        time.sleep(5)

        if generate_random_true25percent():
            driver.find_element_by_xpath(
                '//android.view.ViewGroup[@content-desc="Like button. Double tap and hold to react."]').click()

            time.sleep(5)

        element = driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().scrollable('
                                                             'true).instance(0)).scrollToEnd(1);')

        time.sleep(5)
