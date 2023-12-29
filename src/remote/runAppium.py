import time
import subprocess
import pyautogui as pag
import pygetwindow as gw


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


if is_window_close("Appium"):
    appium_path = "C:/Program Files/Appium/Appium.exe"
    open_application(appium_path)
    perform_action_with_appium()
