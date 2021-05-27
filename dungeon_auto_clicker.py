from auto_clicker import AutoClicker
from images import images
import win32gui
import time


DUNGEONS_LIST = ['dragon', 'fire_knight', 'ice_golem', 'spider']


class DungeonAutoClicker(AutoClicker):
    def __init__(self, dungeon):
        super().__init__()
        self._dungeon = dungeon
        self._nb_runs = 0

        self._im_replay = images['replay']
        self._im_back = images['back']
        self._im_refill = images['refill']
        self._im_dungeon_scroll = images['dungeon_scroll']
        self._im_bastion = images['bastion']
        self._im_battle = images['battle']
        self._im_dungeon = images['dungeon']
        self._im_dungeon_step_5 = images['dungeon_step_5']
        self._im_dungeon_step_14 = images['dungeon_step_14']
        self._im_dungeon_battle_20 = images['dungeon_battle_20']
        self._im_dungeon_battle_start = images['dungeon_battle_start']

        self._im_dungeons = dict(zip(DUNGEONS_LIST, [images[im_name] for im_name in DUNGEONS_LIST]))

    def battle_exists(self):
        return

    def run(self, args):
        self._running = True
        while self._running:
            uid = win32gui.FindWindow(None, "Raid: Shadow Legends")
            try:
                win32gui.SetForegroundWindow(uid)
            except:
                print("ERROR - RSL window not found !")
                self._running = False
                break
            win32gui.MoveWindow(uid, 0, 0, 1280, 720, True)

            self.click_if_present(self._im_battle)
            self.click_if_present(self._im_dungeon)
            self.drag_if_present(self._im_dungeon_scroll, -1000, 0)
            self.click_if_present(self._dungeon)
            self.drag_if_present(self._im_dungeon_step_5, 0, -300)
            self.drag_if_present(self._im_dungeon_step_14, 0, -300)
            self.click_if_present(self._im_dungeon_battle_20)
            self.click_if_present(self._im_dungeon_battle_start)

            if args['REFILL']:
                self.click_if_present(self._im_refill)

            replay = args['NB_RUNS'] == '0' or self._nb_runs < int(args['NB_RUNS'])
            if replay:
                self.click_if_present(self._im_replay)
                self._nb_runs += 1
            else:
                self._running = False

            time.sleep(float(args['FREQUENCY']))
