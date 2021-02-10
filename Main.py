import cv2 as cv
import mouse
import numpy as np
import pyautogui
import threading
import PySimpleGUI as sg
import time


def take_screenshot(file_name='screen.png'):
    image = pyautogui.screenshot()
    image = cv.cvtColor(np.array(image), cv.COLOR_BGR2GRAY)
    return image
    # cv.imwrite("resources/" + file_name, image)
    # return cv.imread("resources/" + file_name, 0)


def check_args(args):
    try:
        freq = float(args['FREQUENCY'])
        return freq >= 0.5
    except:
        return False


class AutoClick:
    def __init__(self):
        self._running = False
        self._template = cv.imread('resources/cat-eye.png', 0)
        self._template_w, self.template_h = self._template.shape[::-1]

    def terminate(self):
        self._running = False

    def run(self, args):
        self._running = True
        while self._running:
            img = take_screenshot()
            cv.imwrite('screen_grayed.png', img)
            res = cv.matchTemplate(img, self._template, cv.TM_CCOEFF_NORMED)
            threshold = 0.95
            position = np.where(res >= threshold)
            if len([p for p in zip(*position[::-1])]) > 0:
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
                top_left = max_loc
                bottom_right = (top_left[0] + self._template_w, top_left[1] + self.template_h)
                mouse_x, mouse_y = mouse.get_position()
                mouse.move((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)
                mouse.click(mouse.LEFT)
                mouse.move(mouse_x, mouse_y)
            time.sleep(float(args['FREQUENCY']))


if __name__ == "__main__":
    layout = [ [sg.Text('Frequency [s]:'), sg.Input(key='FREQUENCY', size=(10, 1)), sg.Text(key='FREQ_ERROR', size=(20, 1))],
            [sg.Button('Start', key='START'), sg.Button('Stop', key='STOP', disabled=True), sg.Text(key='RUNNING', size=(10, 1))] ]

    window = sg.Window('Auto Clicker', layout)

    ac = AutoClick()

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'START':
            args_ok = check_args(values)
            if not args_ok:
                window['FREQ_ERROR'].update('Invalid frequency', text_color='RED')
            else:
                window['FREQ_ERROR'].update('')
                t = threading.Thread(target=ac.run, args=(values,))
                t.start()
                window['START'].update(disabled=True)
                window['STOP'].update(disabled=False)
                window['RUNNING'].update('Running...', text_color='YELLOW')
        elif event == 'STOP':
            window['START'].update(disabled=False)
            window['STOP'].update(disabled=True)
            window['RUNNING'].update('')
            ac.terminate()

    window.close()


#     take_screenshot()
#
#
# img = pyautogui.screenshot()
# img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
# cv.imwrite('resources/screen.png', img)
# img = cv.imread('resources/screen.png', 0)
# template = cv.imread('resources/cat-eye.png', 0)
# w, h = template.shape[::-1]
# res = cv.matchTemplate(img, template, eval('cv.TM_CCOEFF'))
# min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
# top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h)
# mouse.move((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)
