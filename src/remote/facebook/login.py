from appium import webdriver
import os
import time

from src.ld_manager.run_ld import run_ld
from src.services.deviceService import check_device_exists


def login_facebook(data):
    data.device = check_device_exists(data.device)

    run_ld(data.device)
    time.sleep(60)

    desired_cap = {
        "uuid": data.device.uuid,
        "platformName": "Android",
        "appPackage": "com.ldmnq.launcher3",
        "appActivity": "com.android.launcher3.Launcher"
    }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.implicitly_wait(30)

    element = driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Facebook"]')
    element.click()

    element = driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
    element.click()

    element.send_keys(data.email.email_address)

    element = driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
    element.click()

    element.send_keys(data.password)

    element = driver.find_element_by_xpath('//android.view.View[@content-desc="Log in"]')
    element.click()

    element = driver.find_element_by_xpath('//android.widget.Button[@content-desc="Save"]/android.view.ViewGroup')
    element.click()
