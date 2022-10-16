from tkinter import E
import imageio.v3 as iio
import numpy as np
import pygame as pg


class V:

    def __init__(self, path=None) -> None:
        self.display = pg.display.get_surface()

        path = path or 'data/videos/Karuizawa Kei Winter Blanc-1.m4v'
        # self.vid = iio.get_reader(path, format="pyav")
        self.vid = iio.imiter(path, plugin='pyav')

        self.frame = self.get_frame()

        first_frame = next(self.frame)

        ratio = max(
            [l/s for s, l in zip(first_frame.shape[:2], pg.display.get_window_size())])

        self.new_size = [i*ratio for i in first_frame.shape[:2]]

        self.offset = ((np.fromiter(pg.display.get_window_size(
        ), dtype=int) - np.fromiter(self.new_size, dtype=int))//2).tolist()

    def get_frame(self):
        i = 0
        temp = []
        while True:
            for frame in self.vid:
                if i == 0:
                    temp.append(frame)
                yield np.rot90(frame)[::-1]
                
            if i == 0:
                self.vid = temp
                i += 1

    def run(self):
        image = pg.surfarray.make_surface(next(self.frame))
        image = pg.transform.scale(image, self.new_size)
        self.display.blit(image, self.offset)


#writer = iio.get_writer(f"{tail}", fps=12)
