import base64
import time
import subprocess
from appium import webdriver
import pyautogui as pag
import pygetwindow as gw
import os


def perform_action_with_appium():
    while True:
        try:
            window = gw.getWindowsWithTitle("Appium")
            break
        except IndexError:
            time.sleep(1)
    print(f"Window with title Appium found. Performing action...")
    time.sleep(13)
    try:
        window = gw.getWindowsWithTitle("Appium")[0]
        window.activate()
        time.sleep(3)
        image = "C:/Users/Thanh/Desktop/work/social_automation_app/src/remote/img/start-appium.png"
        loc = pag.locateOnScreen(image)
        pag.click(loc)
    except IndexError:
        print(f"Window with title Appium not found")


def open_application(application_path):
    subprocess.Popen(application_path, shell=True)


def is_window_close(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]
        return False
    except IndexError:
        return True


#
# if is_window_close("Appium"):
#     appium_path = "C:/Program Files/Appium/Appium.exe"
#     open_application(appium_path)
#     perform_action_with_appium()


def login_facebook(data):
    desired_cap = {
        "uuid": "emulator-5554",
        "platformName": "Android",
        "appPackage": "com.ldmnq.launcher3",
        "appActivity": "com.android.launcher3.Launcher"
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.implicitly_wait(30)

    element = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Facebook"]')
    element.click()

    element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
    element.click()

    element.send_keys(data.email.email_address)

    element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
    element.click()

    element.send_keys(data.password)

    element = driver.find_element_by_xpath('//android.view.View[@content-desc="Log in"]')
    element.click()