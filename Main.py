import cv2 as cv
import mouse
import numpy as np
import pyautogui
import threading
import PySimpleGUI as sg
import time
import win32gui


def check_args(args):
    try:
        freq = float(args['FREQUENCY'])
        if freq < 0.5:
            return False
        nb_runs = int(args['NB_RUNS'])
        if nb_runs < 0:
            return False
        dung = args['DUNGEON']
        if dung not in ['spider', 'dragon', 'fire_knight', 'ice_golem']:
            return False
        return True
    except:
        return False
        
        
class Image:
    def __init__(self, name):
        self._img = cv.imread('resources/' + name + '.png', 0)
        self._w, self._h = self._img.shape[::-1]
        
        
class ForgeAutoSell:
    def __init__(self):
        self._running = False
        self._screen = None
        self._state = 'init'
        
        self._im_forge = Image('Forge')
        self._im_tenacity = Image('tenacity')
        self._im_perception = Image('perception')
        self._im_3_4 = Image('forge_3_4')
        self._im_buy = Image('forge_buy_3_4')
        self._im_sell = Image('forge_sell')
        self._im_sell_confirm = Image('forge_sell_confirm')
        
    def take_screenshot(self):
        image = pyautogui.screenshot()
        image = cv.cvtColor(np.array(image), cv.COLOR_BGR2GRAY)
        self._screen = image
        
    def coordinates(self, img, threshold=0.95):
        res = cv.matchTemplate(self._screen, img._img, cv.TM_CCOEFF_NORMED)
        threshold = 0.85
        position = np.where(res >= threshold)
        if len([p for p in zip(*position[::-1])]) > 0:
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top_left = max_loc
            bottom_right = (top_left[0] + img._w, top_left[1] + img._h)
            return (top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2, True
        else:
            return 0, 0, False
        
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
        
    def click(self, x, y):
        mouse_x, mouse_y = mouse.get_position()
        mouse.move(x, y)
        mouse.click('left')
        time.sleep(0.5)
        mouse.move(mouse_x, mouse_y)
        
    def terminate(self):
        self._running = False
        
    def run(self):
        self._running = True
        self._state = 'init'
        while self._running:
            uid = win32gui.FindWindow(None, "Raid: Shadow Legends")
            win32gui.SetForegroundWindow(uid)
            win32gui.MoveWindow(uid, 0, 0, 1280, 720, True)
            
            if self._state == 'init':
                self.click_if_present(self._im_forge)
                self.click_if_present(self._im_tenacity)
                if self.click_if_present(self._im_3_4):
                    self._state = 'selling_tenacity'
            elif self._state == 'selling_tenacity':
                self.click_if_present(self._im_buy, wait_time=5.0)
                self.click_if_present(self._im_sell)
                self.click_if_present(self._im_sell_confirm)
            
            time.sleep(0.1)
            


class AutoClick:
    def __init__(self):
        self._running = False
        self._dungeon = 'fire_knight'
        self._screen = None
        self._nb_runs = 0
        
        self._im_replay = Image('replay')
        self._im_back = Image('back')
        self._im_refill = Image('refill')
        self._im_dungeon_scroll =  Image('dungeon_scroll')
        self._im_bastion = Image('bastion')
        self._im_battle = Image('battle')
        self._im_dungeon = Image('dungeon')
        self._im_dungeon_step_5 = Image('dungeon_step_5')
        self._im_dungeon_step_14 = Image('dungeon_step_14')
        self._im_dungeon_battle_20 = Image('dungeon_battle_20')
        self._im_dungeon_battle_start = Image('dungeon_battle_start')
        
        self._im_dungeons = {'dragon': Image('dragon'), 'fire_knight': Image('fire_knight'), 'ice_golem': Image('ice_golem'), 'spider': Image('spider')}
        
    def take_screenshot(self):
        image = pyautogui.screenshot()
        image = cv.cvtColor(np.array(image), cv.COLOR_BGR2GRAY)
        self._screen = image
        
    def set_dungeon(self, d):
        self._dungeon = d

    def terminate(self):
        self._running = False
        
    def coordinates(self, img, threshold=0.95):
        res = cv.matchTemplate(self._screen, img._img, cv.TM_CCOEFF_NORMED)
        threshold = 0.8
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
        
    def drag(self, x, y, dist_x, dist_y, absolute=False, duration=0.1):
        mouse_x, mouse_y = mouse.get_position()
        mouse.move(x, y)
        mouse.drag(0, 0, dist_x, dist_y, absolute, duration)
        time.sleep(0.5)
        mouse.move(mouse_x, mouse_y)

    def run(self, args):
        self._running = True
        while self._running:
            uid = win32gui.FindWindow(None, "Raid: Shadow Legends")
            win32gui.SetForegroundWindow(uid)
            win32gui.MoveWindow(uid, 0, 0, 1280, 720, True)
            
            self.take_screenshot()
            x, y, goto_battle = self.coordinates(self._im_battle)
            if goto_battle:
               self.click(x, y)
               time.sleep(1.0)
            
            self.take_screenshot()
            x, y, goto_dungeon = self.coordinates(self._im_dungeon)
            if goto_dungeon:
                self.click(x, y)
                time.sleep(1.0)
           
            self.take_screenshot()
            x, y, dungeon_scroll = self.coordinates(self._im_dungeon_scroll)
            if dungeon_scroll:
                self.drag(x, y, -1000, 0)
                time.sleep(1.0)
                
            self.take_screenshot()
            x, y, dungeon = self.coordinates(self._im_dungeons[self._dungeon])
            if dungeon:
                self.click(x, y)
                time.sleep(1.0)
                
            self.take_screenshot()
            x, y, dungen_step_5 = self.coordinates(self._im_dungeon_step_5)
            if dungen_step_5:
                self.drag(x, y, 0, -300)
                time.sleep(1.0)
                
            self.take_screenshot()
            x, y, dungen_step_14 = self.coordinates(self._im_dungeon_step_14)
            if dungen_step_14:
                self.drag(x, y, 0, -300)
                time.sleep(1.0)
                
            self.take_screenshot()
            x, y, dungeon_battle_20 = self.coordinates(self._im_dungeon_battle_20)
            if dungeon_battle_20:
                self.click(x, y)
                time.sleep(1.0)
                
            self.take_screenshot()
            x, y, dungeon_battle_start = self.coordinates(self._im_dungeon_battle_start)
            if dungeon_battle_start:
                self.click(x, y)
                time.sleep(1.0)
                
            self.take_screenshot()
            x, y, refill = self.coordinates(self._im_refill)
            if refill and args['REFILL']:
                self.click(x, y)
                time.sleep(1.0)
                
            self.take_screenshot()
            x, y, replay = self.coordinates(self._im_replay)
            if replay and (args['NB_RUNS'] == '0' or self._nb_runs < int(args['NB_RUNS'])):
                self.click(x, y)
                time.sleep(1.0)
                self.take_screenshot()
                x, y, replay = self.coordinates(self._im_replay)
                if not replay:
                    self._nb_runs += 1
                    if int(args['NB_RUNS']) != 0 and self._nb_runs >= int(args['NB_RUNS']):
                        self._running = False
                
            time.sleep(float(args['FREQUENCY']))


if __name__ == "__main__":
    layout = [ [sg.Text('Dungeon:'), sg.Input('fire_knight', key='DUNGEON')],
            [sg.Text('Frequency [s]:'), sg.Input('5', key='FREQUENCY', size=(10, 1)), sg.Text(key='FREQ_ERROR', size=(20, 1))],
            [sg.Text('Nb runs: '), sg.Input('0', key='NB_RUNS'), sg.Checkbox('Refill', key='REFILL')],
            [sg.Button('Start', key='START'), sg.Button('Stop', key='STOP', disabled=True), sg.Text(key='RUNNING', size=(10, 1))],
            [sg.Text('Forge Auto Sell')],
            [sg.Button('Start', key='START_FORGE'), sg.Button('Stop', key='STOP_FORGE', disabled=True)] ]

    window = sg.Window('Auto Clicker', layout)

    ac = AutoClick()
    fas = ForgeAutoSell()

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
                ac._dungeon = values['DUNGEON']
                ac_nb_runs = 0
                t = threading.Thread(target=ac.run, args=(values,))
                t.start()
                window['START'].update(disabled=True)
                window['STOP'].update(disabled=False)
                window['RUNNING'].update('Running...', text_color='YELLOW')
                window['START_FORGE'].update(disabled=True) 
        elif event == 'STOP' or (event is None and not ac._running):
            window['START'].update(disabled=False)
            window['STOP'].update(disabled=True)
            window['RUNNING'].update('')
            window['START_FORGE'].update(disabled=False)
            ac.terminate()
        elif event == 'START_FORGE':
            window['START'].update(disabled=True)
            window['START_FORGE'].update(disabled=True)
            window['STOP_FORGE'].update(disabled=False)
            fas_t = threading.Thread(target=fas.run)
            fas_t.start()
        elif event == 'STOP_FORGE' or not fas._running:
            window['START'].update(disabled=False)
            window['START_FORGE'].update(disabled=False)
            window['STOP_FORGE'].update(disabled=True)
            fas.terminate()

    window.close()
