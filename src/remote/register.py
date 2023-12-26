from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
from appium.webdriver.common.mobileby import MobileBy
from PIL import Image
import base64
import requests
import pyautogui as pag
import pygetwindow as gw
import subprocess


def text_to_keycodes(text, driver):
    for char in text:
        print(ord(char))
        if (58 > ord(char) > 47):
            keycode = ord(char) + 96
            driver.press_keycode(keycode)
        else:
            keycode = ord(char) - 68
            driver.press_keycode(keycode)


def press_next_btn(driver):
    screenshot_path = "./img/screenshot.png"
    driver.get_screenshot_as_file(screenshot_path)
    original_image = Image.open(screenshot_path)
    crop_region = (70, 480, 680, 580)
    cropped_image = original_image.crop(crop_region)
    cropped_image.save("./img/check-point.png")
    cropped_image.save("./img/check-point-scope.png")
    original_checkpoint = Image.open("./img/check-point.png")
    original_checkpoint = base64.b64encode(original_checkpoint.tobytes()).decode('utf-8')
    scope_checkpoint = Image.open("./img/check-point-scope.png")
    scope_checkpoint = base64.b64encode(scope_checkpoint.tobytes()).decode('utf-8')
    while (original_checkpoint == scope_checkpoint):
        time.sleep(3)
        screenshot_path = "./img/screenshot.png"
        driver.get_screenshot_as_file(screenshot_path)
        original_image = Image.open(screenshot_path)
        crop_region = (70, 480, 680, 580)
        cropped_image = original_image.crop(crop_region)
        cropped_image.save("./img/check-point-scope.png")
        scope_checkpoint = Image.open("./img/check-point-scope.png")
        scope_checkpoint = base64.b64encode(scope_checkpoint.tobytes()).decode('utf-8')
        if (original_checkpoint == scope_checkpoint):
            driver.find_element_by_xpath('//android.widget.Button[@content-desc="Tiếp"]/android.view.ViewGroup').click()


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        return encoded_image.decode("utf-8")


def capture_captcha(driver):
    screenshot_path = "./img/screenshot.png"
    driver.get_screenshot_as_file(screenshot_path)
    original_image = Image.open(screenshot_path)
    crop_region = (70, 400, 680, 580)
    cropped_image = original_image.crop(crop_region)
    cropped_image.save("./img/captcha.png")
    base64_img = encode_image_to_base64("./img/captcha.png")
    data = {
        "api_token": "9EBLeUD05kDQbhUqArbUpOr34rzhcWAumxkaMf4SPHXcUGpkaeelFYm7foBxH9v2j0TRuYNWLtgp4gBO",
        "data": {
            "type_job_id": "30",
            "image_base64": base64_img
        }
    }
    response = requests.post("https://omocaptcha.com/api/createJob", json=data)
    if response.status_code != None:
        response = response.json()
        print(response)
        job_id = response['job_id']
        request_data = {
            "api_token": "9EBLeUD05kDQbhUqArbUpOr34rzhcWAumxkaMf4SPHXcUGpkaeelFYm7foBxH9v2j0TRuYNWLtgp4gBO",
            "job_id": job_id
        }
        time.sleep(10)
        response = requests.post("https://omocaptcha.com/api/getJobResult", json=request_data)
        response = response.json()
        print(response)
        return response['result']
    else:
        print(f"Error: {response.status_code}")


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


class User:
    def __init__(self, password_email, email, name, surname, uuid, password):
        self.email = email
        self.password_email = password_email
        self.name = name
        self.surname = surname
        self.uuid = uuid
        self.password = password


user = User(
    email="snssssss123@nikolaxflem.com",
    password_email="12345678",
    name="Thanh",
    surname="Pham",
    uuid="emulator-5558",
    password="Danny@0311"
)


def registerFacebook(userData):
    desired_cap = {
        "uuid": user.uuid,
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
    driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Aqua Mail"]').click()

    try:
        driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.View').click()
    except NoSuchElementException:
        print("NOT FOUND")

    driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[5]').click()

    element = driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.ViewFlipper/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout/android.widget.EditText')
    element.click()
    element.send_keys(user.email)

    element = driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.ViewFlipper/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.FrameLayout/android.widget.EditText')
    element.click()
    element.send_keys(user.password_email)

    driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.TextView[3]').click()
    element = driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.ViewFlipper/android.view.ViewGroup/android.widget.LinearLayout[1]/android.widget.FrameLayout/android.widget.EditText')
    element.click()
    element.send_keys(user.surname + " " + user.name)

    driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.TextView[3]').click()

    element_text = 'Skip'
    element_locator = (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{}")'.format(element_text))
    element = driver.find_element(*element_locator)
    element.click()
    driver.press_keycode(27)

    time.sleep(3)
    try:
        driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button[2]').click()
    except NoSuchElementException:
        print("ERROR")
    finally:
        time.sleep(3)
        # driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[1]').click()
        driver.tap([(8, 104), (104, 200)], 200)
        driver.quit()

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.implicitly_wait(30)
    time.sleep(2)
    driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Facebook"]').click()
    time.sleep(10)

    screenshot_path = "./img/screenshot.png"
    driver.get_screenshot_as_file(screenshot_path)
    original_image = Image.open(screenshot_path)
    crop_region = (70, 240, 380, 280)
    cropped_image = original_image.crop(crop_region)
    cropped_image.save("./img/check-point-scope.png")
    original_checkpoint = Image.open("./img/email-validate.png")
    original_checkpoint = base64.b64encode(original_checkpoint.tobytes()).decode('utf-8')
    scope_checkpoint = Image.open("./img/check-point-scope.png")
    scope_checkpoint = base64.b64encode(scope_checkpoint.tobytes()).decode('utf-8')
    time.sleep(5)
    if original_checkpoint == scope_checkpoint:
        driver.quit()
        print("TRUE")
        time.sleep(5)
    else:
        driver.find_element_by_xpath(
            '//android.widget.Button[@content-desc="Tạo tài khoản mới"]/android.view.ViewGroup').click()
        time.sleep(2)
        driver.find_element_by_xpath('//android.widget.Button[@content-desc="Bắt đầu"]/android.view.ViewGroup').click()
        time.sleep(2)

        element = driver.find_element_by_xpath(
            '//android.widget.LinearLayout[@content-desc="Chọn tài khoản"]/android.widget.LinearLayout/android.widget.Button')
        element.click()

        element = driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
        element.click()
        element.send_keys(user.surname)

        element = driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
        element.click()
        element.send_keys(user.name)

        press_next_btn(driver)

        time.sleep(3)
        driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.Button[1]").click()

        time.sleep(2)
        driver.find_element_by_xpath('//android.widget.Button[@content-desc="Tiếp"]/android.view.ViewGroup').click()
        time.sleep(1)
        driver.find_element_by_xpath('//android.widget.Button[@content-desc="Tiếp"]/android.view.ViewGroup').click()
        time.sleep(1)
        element = driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
        element.click()
        element.send_keys(random.randint(20, 35))

        press_next_btn(driver)
        time.sleep(1)
        driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.Button[1]').click()

        time.sleep(1)
        driver.find_element_by_xpath(
            '//android.widget.Button[@content-desc="Nam"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView').click()
        time.sleep(1)
        press_next_btn()
        time.sleep(1)
        driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button[1]").click()
        time.sleep(1)
        driver.find_element_by_xpath(
            '//android.widget.Button[@content-desc="Đăng ký bằng email"]/android.view.ViewGroup').click()
        element = driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
        element.click()
        element.send_keys(user.email)
        time.sleep(2)

        screenshot_path = "./img/screenshot.png"
        driver.get_screenshot_as_file(screenshot_path)
        original_image = Image.open(screenshot_path)
        crop_region = (70, 500, 680, 680)
        cropped_image = original_image.crop(crop_region)
        cropped_image.save("./img/check-point.png")
        cropped_image.save("./img/check-point-scope.png")
        original_checkpoint = Image.open("./img/check-point.png")
        original_checkpoint = base64.b64encode(original_checkpoint.tobytes()).decode('utf-8')
        scope_checkpoint = Image.open("./img/check-point-scope.png")
        scope_checkpoint = base64.b64encode(scope_checkpoint.tobytes()).decode('utf-8')
        while (original_checkpoint == scope_checkpoint):
            screenshot_path = "./img/screenshot.png"
            driver.get_screenshot_as_file(screenshot_path)
            original_image = Image.open(screenshot_path)
            crop_region = (70, 500, 680, 680)
            cropped_image = original_image.crop(crop_region)
            cropped_image.save("./img/check-point-scope.png")
            scope_checkpoint = Image.open("./img/check-point-scope.png")
            scope_checkpoint = base64.b64encode(scope_checkpoint.tobytes()).decode('utf-8')
            if (original_checkpoint == scope_checkpoint):
                driver.find_element_by_xpath(
                    '//android.widget.Button[@content-desc="Tiếp"]/android.view.ViewGroup').click()
            time.sleep(3)

        element = driver.find_element_by_xpath(
            '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
        element.click()
        element.send_keys(user.password)
        time.sleep(5)

        press_next_btn(driver)

        driver.find_element_by_xpath('//android.view.View[@content-desc="Lưu"]').click()
        time.sleep(3)
        driver.find_element_by_xpath('//android.view.View[@content-desc="Tôi đồng ý"]').click()
        time.sleep(30)

        # ---------------------------------------- Captcha ----------------------------------------
        screenshot_path = "./img/screenshot.png"
        driver.get_screenshot_as_file(screenshot_path)
        original_image = Image.open(screenshot_path)
        crop_region = (70, 240, 380, 280)
        cropped_image = original_image.crop(crop_region)
        cropped_image.save("./img/check-point-scope.png")
        original_checkpoint = Image.open("./img/email-validate.png")
        original_checkpoint = base64.b64encode(original_checkpoint.tobytes()).decode('utf-8')
        scope_checkpoint = Image.open("./img/check-point-scope.png")
        scope_checkpoint = base64.b64encode(scope_checkpoint.tobytes()).decode('utf-8')
        original_checkpoint2 = Image.open("./img/email-validate2.png")
        original_checkpoint2 = base64.b64encode(original_checkpoint2.tobytes()).decode('utf-8')
        if (original_checkpoint == scope_checkpoint or original_checkpoint2 == scope_checkpoint):

            driver.quit()

        else:
            print("FAILED")
            driver.find_element_by_xpath('//android.view.ViewGroup[@content-desc="Tiếp tục"]').click()
            time.sleep(3)
            screenshot_path = "./img/screenshot.png"
            driver.get_screenshot_as_file(screenshot_path)
            original_image = Image.open(screenshot_path)
            crop_region = (70, 600, 680, 680)
            cropped_image = original_image.crop(crop_region)
            cropped_image.save("./img/check-point.png")
            cropped_image.save("./img/check-point-scope.png")
            original_checkpoint = Image.open("./img/check-point.png")
            original_checkpoint = base64.b64encode(original_checkpoint.tobytes()).decode('utf-8')
            scope_checkpoint = Image.open("./img/check-point-scope.png")
            scope_checkpoint = base64.b64encode(scope_checkpoint.tobytes()).decode('utf-8')
            while (original_checkpoint == scope_checkpoint):
                screenshot_path = "./img/screenshot.png"
                driver.get_screenshot_as_file(screenshot_path)
                original_image = Image.open(screenshot_path)
                crop_region = (70, 600, 680, 680)
                cropped_image = original_image.crop(crop_region)
                cropped_image.save("./img/check-point-scope.png")
                scope_checkpoint = Image.open("./img/check-point-scope.png")
                scope_checkpoint = base64.b64encode(scope_checkpoint.tobytes()).decode('utf-8')
                if (original_checkpoint == scope_checkpoint):
                    screenshot_path = "./img/screenshot.png"
                    driver.get_screenshot_as_file(screenshot_path)
                    original_image = Image.open(screenshot_path)
                    crop_region = (70, 400, 680, 580)
                    cropped_image = original_image.crop(crop_region)
                    cropped_image.save("./img/captcha.png")
                    base64_img = encode_image_to_base64("./img/captcha.png")
                    data = {
                        "api_token": "9EBLeUD05kDQbhUqArbUpOr34rzhcWAumxkaMf4SPHXcUGpkaeelFYm7foBxH9v2j0TRuYNWLtgp4gBO",
                        "data": {
                            "type_job_id": "30",
                            "image_base64": base64_img
                        }
                    }
                    response = requests.post("https://omocaptcha.com/api/createJob", json=data)
                    if response.status_code != None:
                        response = response.json()
                        print(response)
                        job_id = response['job_id']
                        request_data = {
                            "api_token": "9EBLeUD05kDQbhUqArbUpOr34rzhcWAumxkaMf4SPHXcUGpkaeelFYm7foBxH9v2j0TRuYNWLtgp4gBO",
                            "job_id": job_id
                        }
                        time.sleep(30)
                        response = requests.post("https://omocaptcha.com/api/getJobResult", json=request_data)
                        if response.status_code != None:
                            response = response.json()
                            print(response)
                        else:
                            driver.quit()

                    time.sleep(1)
                    driver.press_keycode(61)
                    time.sleep(1)
                    driver.press_keycode(61)
                    time.sleep(1)
                    driver.press_keycode(61)
                    time.sleep(1)
                    driver.press_keycode(61)
                    time.sleep(1)
                    driver.press_keycode(61)
                    time.sleep(1)
                    driver.press_keycode(61)
                    time.sleep(1)
                    driver.press_keycode(61)
                    time.sleep(1)

                    driver.press_keycode(67)
                    driver.press_keycode(67)
                    driver.press_keycode(67)
                    driver.press_keycode(67)
                    driver.press_keycode(67)
                    driver.press_keycode(67)
                    time.sleep(5)
                    text_to_keycodes(response['result'], driver)
                    driver.press_keycode(61)
                    driver.find_element_by_xpath('//android.view.ViewGroup[@content-desc="Tiếp tục"]').click()
                    time.sleep(3)

            element = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.EditText')
            element.click()
            element.send_keys(user.email)
            driver.find_element_by_xpath('//android.view.ViewGroup[@content-desc="Gửi mã đăng nhập"]').click()
            time.sleep(3)
            driver.quit()

    # KICH HOAT
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.implicitly_wait(30)
    driver.find_element_by_xpath('//android.widget.TextView[@content-desc="Aqua Mail"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//android.widget.ImageView[@content-desc="Tùy chọn khác"]').click()
    time.sleep(1)
    driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.TextView[1]').click()
    time.sleep(3)
    driver.press_keycode(27)
    driver.press_keycode(27)
    time.sleep(3)
    driver.find_element_by_xpath(
        '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[4]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.recyclerview.aquamail.RecyclerView/org.kman.AquaMail.view.AbsMessageListItemLayout[1]').click()

    driver.press_keycode(27)
    time.sleep(3)
    driver.press_keycode(61)
    driver.press_keycode(61)
    driver.press_keycode(61)
    driver.press_keycode(61)
    driver.press_keycode(61)
    driver.press_keycode(66)
    time.sleep(10)
