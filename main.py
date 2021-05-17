import pytesseract
from PIL import ImageGrab, Image
import time
import keyboard
import re
import numpy as np


class MathBot:
    def __init__(self):
        self.run = True

    def exit_(self):
        self.run = False

    def main(self):
        # Make it so we're able to quit
        keyboard.add_hotkey("f8", self.exit_)

        # Setup tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

        while self.run:
            equation = pytesseract.image_to_string(self.get_equation_image(),
                                                   config="--oem 1 --psm 7 -c tessedit_char_whitelist=1234567890+-=")
            # Remove the "=" and other various characters from the equation
            equation = equation.strip()
            equation = equation[:-1]
            # Check if the equation is valid
            if re.search(r"\d\W\d", equation):
                # Compute the answer to the equation
                answer = eval(equation)
                # Enter the equation on the GUI
                self.enter_answer(str(answer))
                # Delay cause the numbers take time to regenerate
                time.sleep(0.015)

    @staticmethod
    def get_equation_image():
        """Screenshots the screen, crops the equation, alters it for tesseract, and then returns it"""
        # Crop dimensions
        x = 25
        left_offset = 400 - x
        upper_offset = 150
        image_width = 500 + x
        image_height = 115 * 2
        crop_cords = (left_offset, upper_offset, left_offset + image_width, upper_offset + image_height)

        # Screenshot the screen and crop the image
        img = ImageGrab.grab().crop(crop_cords)

        # Turn the image background to black so tesseract will have an easier time reading it
        img.convert("RGBA")
        data = np.array(img)

        red, green, blue = data.T
        not_white_ares = (red != 255) & (blue != 255) & (green != 255)

        data[...][not_white_ares.T] = (0, 0, 0)

        img = Image.fromarray(data)

        return img

    @staticmethod
    def enter_answer(answer: str):
        """Enters the given answer into the answer bar"""
        keyboard.write(answer)
        keyboard.press_and_release("enter")


if __name__ == '__main__':
    math_bot = MathBot()
    math_bot.main()
