import imageio as iio
import os
import numpy as np
import pygame as pg

path = 'data/videos/Karuizawa Kei Winter Blanc-1.m4v'

vid = iio.get_reader(path, format="FFMPEG")

frames = []
_, tail = os.path.split(path)

def get_frame():
    while True:
        for frame in vid:
            yield np.rot90(frame)[::-1]




class V:
    def __init__(self, display: pg.Surface) -> None:
        self.display = display
        self.frame = get_frame()

        first_frame  = next(self.frame)

        ratio = max([l/s for s, l in zip(first_frame.shape[:2], pg.display.get_window_size())])

        self.new_size = [i*ratio for i in first_frame.shape[:2]]

        self.offset = ((np.fromiter(pg.display.get_window_size(), dtype=int) - np.fromiter(self.new_size, dtype=int) )//2).tolist()


    def run(self):
        image = pg.surfarray.make_surface(next(self.frame))
        image = pg.transform.scale(image, self.new_size)
        self.display.blit(image, self.offset)






#writer = iio.get_writer(f"{tail}", fps=12)

