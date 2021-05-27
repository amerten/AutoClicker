import cv2 as cv
import mouse
import numpy as np
import time
import pyautogui


class AutoClicker:
    def __init__(self):
        self._running = False
        self._screen = None

    def take_screenshot(self):
        image = pyautogui.screenshot()
        image = cv.cvtColor(np.array(image), cv.COLOR_BGR2GRAY)
        self._screen = image

    def terminate(self):
        self._running = False

    def coordinates(self, img, threshold=0.95):
        res = cv.matchTemplate(self._screen, img._img, cv.TM_CCOEFF_NORMED)
        position = np.where(res >= threshold)
        if len([p for p in zip(*position[::-1])]) > 0:
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0] + img._w, top_left[1] + img._h)
            return (top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2, True
        else:
            return 0, 0, False

    def click(self, x, y):
        mouse_x, mouse_y = mouse.get_position()
        mouse.move(x, y)
        mouse.click('left')
        time.sleep(0.5)
        mouse.move(mouse_x, mouse_y)

    def click_if_present(self, im, wait_time=1.0, stop_if_missing=False):
        self.take_screenshot()
        x, y, present = self.coordinates(im)
        if present:
            self.click(x, y)
            time.sleep(wait_time)
            return True
        if stop_if_missing:
            self._running = False
        return False

    def drag_if_present(self, im, delta_x, delta_y, wait_time=1.0, stop_if_missing=False):
        self.take_screenshot()
        x, y, present = self.coordinates(im)
        if present:
            self.drag(x, y, delta_x, delta_y)
            time.sleep(wait_time)
            return True
        if stop_if_missing:
            self._running = False
        return False

    def drag(self, x, y, dist_x, dist_y, absolute=False, duration=0.1):
        mouse_x, mouse_y = mouse.get_position()
        mouse.move(x, y)
        mouse.drag(0, 0, dist_x, dist_y, absolute, duration)
        time.sleep(0.5)
        mouse.move(mouse_x, mouse_y)

    def run(self, args):
        print("Implement this abstract method")