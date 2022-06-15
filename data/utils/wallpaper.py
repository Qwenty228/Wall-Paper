import pygame as pg
import win32gui, win32con
import asyncio
from data.utils.config import FPS

from data.utils.worker import Window
from data.template import video



class WallPaper:
    def __init__(self) -> None:
        self.wm = Window()
        self.wm.get_workerw()
        self.mainClock = pg.time.Clock()
        self._clip_surface()


    def _clip_surface(self):
        win32gui.ShowWindow(self.wm.WorkerW, win32con.SW_MAXIMIZE)
        self.screen = pg.display.set_mode((0, 0), flags=pg.HIDDEN|pg.SRCALPHA, vsync=1)
        win32gui.SetParent(pg.display.get_wm_info()['window'], self.wm.WorkerW)
        self.screen = pg.display.set_mode((0, 0), flags=pg.SHOWN|pg.SRCALPHA, vsync=1)


    async def draw(self, mode, selection):
        if mode == 0:
            func = video.V(selection)
        running = True
        pg.event.pump()
        #i = 0
        while running:
            self.mainClock.tick(FPS)
            #i += 1
            #print(i)
            #print('Running')
            func.run()
            pg.display.flip()
            await asyncio.sleep(0)
            #     pg.event.pump()

            #     func.run()
            
            #     pg.display.flip()
            # except Exception as e:
            #     print(Exception)
            #     running = False

            # await asyncio.sleep(0)

        # self.wm.kill_workerw()
            
        # print('quit')
        # quit()
            
