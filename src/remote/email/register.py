import random
import time

from appium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError

from src.enum.EmailEnum import EmailEnum
from src.utils.findText import get_email_type
from src.utils.imageUtils import capture_checkpoint


def register_email():
    desired_cap = {
        "udid": "emulator-5564",
        "platformName": "Android",
        "appPackage": "com.ldmnq.launcher3",
        "appActivity": "com.android.launcher3.Launcher"
    }

    while True:
        try:
            driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
            driver.implicitly_wait(30)

            driver.find_element(By.XPATH, '//android.widget.FrameLayout[@content-desc="Folder: System '
                                          'Apps"]/android.widget.ImageView').click()
            driver.find_element(By.XPATH, '//android.widget.TextView[@content-desc="Settings"]').click()
            driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().scrollable(true).instance('
                                                       '0)).scrollIntoView(new UiSelector().text('
                                                       '"Accounts").instance(0));')
            time.sleep(2)
            driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                          '.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                                          '/android.widget.LinearLayout/android.widget.FrameLayout['
                                          '2]/android.support.v7.widget.RecyclerView/android.widget.LinearLayout['
                                          '4]/android.widget.LinearLayout/android.widget.TextView[1]').click()
            driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                          '.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                                          '/android.widget.LinearLayout/android.widget.LinearLayout/android.widget'
                                          '.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout'
                                          '/android.support.v7.widget.RecyclerView/android.widget.LinearLayout['
                                          '1]/android.widget.LinearLayout/android.widget.RelativeLayout').click()

            if get_email_type("Brilliantedee8903973608@gmail.com") == EmailEnum.GMAIL.value:
                register_gmail(driver=driver)

            return driver

        except MaxRetryError:
            continue

        except WebDriverException as e:
            print(f"Error: {e}")
            continue


def register_gmail(driver, data=None):
    driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                  '.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget'
                                  '.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android'
                                  '.widget.LinearLayout/android.widget.FrameLayout/android.support.v7.widget'
                                  '.RecyclerView/android.widget.LinearLayout['
                                  '8]/android.widget.LinearLayout/android.widget.RelativeLayout').click()
    driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                  '.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                  '.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                  '.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View'
                                  '/android.view.View/android.view.View[6]/android.view.View/android.view.View').click()
    driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                  '.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                  '.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                  '.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View'
                                  '/android.view.View/android.view.View[6]/android.view.View['
                                  '2]/android.view.View/android.view.MenuItem[1]').click()

    driver.press_keycode(61)
    time.sleep(2)
    first_name = driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout'
                                               '/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                               '.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout'
                                               '/android.widget.LinearLayout/android.widget.FrameLayout/android'
                                               '.webkit.WebView/android.webkit.WebView/android.view.View/android.view'
                                               '.View/android.view.View[4]/android.view.View/android.view.View['
                                               '1]/android.view.View/android.view.View[1]/android.widget.EditText')
    first_name.click()
    first_name.send_keys('Nguyễn')

    time.sleep(2)
    driver.press_keycode(61)
    time.sleep(2)

    actions = ActionChains(driver)
    actions.send_keys('Diễm Trinh')

    time.sleep(2)

    driver.find_element(By.CLASS_NAME, 'android.widget.Button').click()
    month = driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                          '.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout'
                                          '/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                          '.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android'
                                          '.webkit.WebView/android.view.View/android.view.View/android.view.View['
                                          '4]/android.view.View/android.view.View[1]/android.view.View['
                                          '2]/android.view.View')
    month.click()
    month = driver.find_element(By.XPATH, f'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android'
                                          f'.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                          f'.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android'
                                          f'.widget.CheckedTextView[{random.randint(1, 10)}]')
    month.click()
    day = driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                        '.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout'
                                        '/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                        '.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android'
                                        '.webkit.WebView/android.view.View/android.view.View/android.view.View['
                                        '4]/android.view.View/android.view.View[2]/android.view.View['
                                        '1]/android.widget.EditText')
    day.click()
    day.send_keys("03")
    year = driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                         '.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout'
                                         '/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                         '.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android'
                                         '.webkit.WebView/android.view.View/android.view.View/android.view.View['
                                         '4]/android.view.View/android.view.View[3]/android.view.View['
                                         '1]/android.widget.EditText')
    year.click()
    year.send_keys("1994")
    gender = driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                           '.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout'
                                           '/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                           '.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android'
                                           '.webkit.WebView/android.view.View/android.view.View/android.view.View['
                                           '4]/android.view.View/android.view.View[4]/android.view.View['
                                           '2]/android.view.View')
    gender.click()
    gender_male = driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout'
                                                '/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                                '.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                                '.ListView/android.widget.CheckedTextView[2]')
    gender_male.click()
    driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                  '.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                  '.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                  '.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View'
                                  '/android.view.View/android.view.View['
                                  '5]/android.view.View/android.widget.Button').click()
    driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                  '.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                  '.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget'
                                  '.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View['
                                  '2]/android.view.View[3]/android.view.View/android.view.View/android.view.View['
                                  '3]').click()
    email = driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android'
                                          '.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout'
                                          '/android.widget.FrameLayout/android.widget.FrameLayout/android.widget'
                                          '.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android'
                                          '.webkit.WebView/android.view.View[2]/android.view.View['
                                          '3]/android.view.View/android.view.View[2]/android.view.View['
                                          '1]/android.widget.EditText')
    email.click()
    email.send_keys("Brilliantedee8903973608")


register_email()
