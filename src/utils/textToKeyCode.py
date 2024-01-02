import time


def text_to_keycodes(text, driver):
    for char in text:
        time.sleep(1)
        if 58 > ord(char) > 47:
            keycode = ord(char) - 41
            driver.press_keycode(keycode)

        elif ord(char) == 64:
            driver.press_keycode(77)

        elif ord(char) == 46:
            driver.press_keycode(56)

        elif ord(char) == 45:
            driver.press_keycode(69)

        elif ord(char) == 160:
            driver.press_keycode(62)

        elif 91 > ord(char) > 64:
            args_map = {'action': char}
            driver.execute_script("mobile: performEditorAction", args_map)

        else:
            keycode = ord(char) - 68
            driver.press_keycode(keycode)
