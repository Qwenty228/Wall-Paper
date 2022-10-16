import pygame as pg
import win32gui, win32con
import asyncio
import importlib

from data.utils.config import FPS

from data.utils.worker import Window
from data.template import video



class WallPaper:
    def __init__(self) -> None:
        self.wm = Window()
        self.wm.get_workerw()
        self.mainClock = pg.time.Clock()
        self._clip_surface()
        self.running = True


    def _clip_surface(self):
        win32gui.ShowWindow(self.wm.WorkerW, win32con.SW_MAXIMIZE)
        self.screen = pg.display.set_mode((0, 0), flags=pg.HIDDEN|pg.SRCALPHA, vsync=1)
        win32gui.SetParent(pg.display.get_wm_info()['window'], self.wm.WorkerW)
        self.screen = pg.display.set_mode((0, 0), flags=pg.SHOWN|pg.SRCALPHA, vsync=1)

    def pause(self):
        self.running = not self.running
        self.wm.toggle_workerw_visibility()

    async def draw(self, mode, selection):
        if mode == 0:
            func = video.V(selection)
        elif mode == 1:
            func = importlib.import_module(selection).G()
        pg.event.pump()
        
        while True:
            self.mainClock.tick(FPS)
            # print(self.mainClock.get_fps())
           
            if self.running:
                func.run()
                pg.display.flip()
            await asyncio.sleep(0)

