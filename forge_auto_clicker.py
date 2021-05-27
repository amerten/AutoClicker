from auto_clicker import AutoClicker
from images import images
import win32gui
import time


class ForgeAutoClicker(AutoClicker):
    def __init__(self):
        super().__init__()
        self._state = 'init'

        self._im_forge = images['forge']
        self._im_tenacity = images['tenacity']
        self._im_perception = images['perception']
        self._im_3_4 = images['forge_3_4']
        self._im_buy = images['forge_buy_3_4']
        self._im_sell = images['forge_sell']
        self._im_sell_confirm = images['forge_sell_confirm']

    def run(self, args):
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