from appium import webdriver
import base64
import time
from appium.webdriver.common.mobileby import MobileBy
import subprocess
import pyautogui as pag
import pygetwindow as gw


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        return encoded_image.decode("utf-8")


def open_application(application_path):
    subprocess.Popen(application_path, shell=True)


def is_window_close(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]
        return False
    except IndexError:
        return True


def perform_action_with_appium():
    while True:
        try:
            window = gw.getWindowsWithTitle("Appium")[0]
            break
        except IndexError:
            time.sleep(1)
    print(f"Window with title Appium found. Performing action...")
    time.sleep(3)
    try:
        window = gw.getWindowsWithTitle("Appium")[0]
        window.activate()
        time.sleep(3)
        image = 'img/start-appium.png'
        loc = pag.locateOnScreen(image)
        pag.click(loc)
    except IndexError:
        print(f"Window with title Appium not found")


desired_cap = {
    "uuid": "emulator-5554",
    "platformName": "Android",
    "appPackage": "com.ldmnq.launcher3",
    "appActivity": "com.android.launcher3.Launcher"
}

if is_window_close("Appium"):
    appium_path = "C:/Users/acer/AppData/Local/Programs/Appium/Appium.exe"
    open_application(appium_path)
    perform_action_with_appium()

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
driver.implicitly_wait(30)

element = driver.find_element_by_id("com.ldmnq.launcher3:id/preview_background")
element.click()

element = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Cài đặt"]')
element.click()

time.sleep(5)
driver.find_element_by_android_uiautomator(
    'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("Tài khoản").instance(0));')
element_text = 'Tài khoản'
element_resource_id = 'android:id/title'
element_locator = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("{}").resourceId("{}")'.format(element_text, element_resource_id))
driver.find_element(*element_locator).click()

element_text = 'Thêm tài khoản'
element_resource_id = 'android:id/title'
element_locator = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("{}").resourceId("{}")'.format(element_text, element_resource_id))
driver.find_element(*element_locator).click()

time.sleep(5)

element_text = ''
element_resource_id = 'identifierId'
element_locator = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("{}").resourceId("{}")'.format(element_text, element_resource_id))
element = driver.find_element(*element_locator)
element.click()
element.send_keys("baosaigon56@gmail.com")

element_text = ''
element_resource_id = 'identifierNext'
element_locator = (
    MobileBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("{}").resourceId("{}")'.format(element_text, element_resource_id))
element = driver.find_element(*element_locator)
element.click()
time.sleep(5)

element = driver.find_element_by_class_name("android.widget.EditText")
element.click()
element.send_keys("Nhuthao123?")
time.sleep(3)

element_text = 'Tiếp theo'
element_locator = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{}")'.format(element_text))
element = driver.find_element(*element_locator)
element.click()
element.click()
time.sleep(3)

element_text = 'Tôi đồng ý'
element_locator = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{}")'.format(element_text))
element = driver.find_element(*element_locator)
element.click()

time.sleep(3)
driver.quit()

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
driver.implicitly_wait(30)

time.sleep(3)
element = driver.find_element_by_id("com.ldmnq.launcher3:id/searchInputView")
element.click()

time.sleep(3)
element = driver.find_element_by_id("com.android.ld.appstore:id/et_search")
element.click()

element.send_keys("facebook")
driver.press_keycode(66)

time.sleep(3)
driver.find_element_by_id("com.android.ld.appstore:id/searchResult_list_icon").click()

encoded = encode_image_to_base64("./img/caidat.png")
element = driver.find_element_by_id("com.android.ld.appstore:id/tv_download_status")
element_encoded = element.screenshot_as_base64.replace('\n.\ldconsole', '')

if element_encoded == encoded:
    element.click()
    time.sleep(2)
    driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.Button").click()
    time.sleep(20)
    driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Điều hướng lên"]').click()

time.sleep(5)
driver.find_element_by_xpath(
    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[1]/android.view.View').click()

time.sleep(5)
element = driver.find_element_by_xpath(
    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.EditText")
element.click()
element.send_keys("aqua mail")
driver.press_keycode(66)

time.sleep(2)
driver.find_element_by_xpath('//android.widget.Button[@content-desc="Cài đặt"]').click()
time.sleep(15)
driver.quit()
