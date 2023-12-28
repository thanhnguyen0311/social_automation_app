import base64
from PIL import Image
from io import BytesIO
import pytesseract

from src.constants.constants import pytesseract_PATH


def find_text_in_screenshot(driver, input_text):
    pytesseract.pytesseract.tesseract_cmd = pytesseract_PATH

    screenshot_base64 = driver.get_screenshot_as_base64()
    screenshot_bytes = base64.b64decode(screenshot_base64)
    screenshot = Image.open(BytesIO(screenshot_bytes))
    text = pytesseract.image_to_string(screenshot)
    index = text.find(input_text)
    if index != -1:
        return True
    else:
        return False