import imageio.v3 as iio
import pygame as pg
import numpy as np
from data.base import BaseAnim


class Anim(BaseAnim):
    def __init__(self):
        self.img_generator = iio.imiter("test/Karuizawa Kei Winter Blanc-1.m4v")

    def update(self, **kwargs):
        try:
            img = next(self.img_generator)
        except StopIteration:
            self.img_generator = iio.imiter("test/Karuizawa Kei Winter Blanc-1.m4v")
            img = next(self.img_generator)
        return pg.surfarray.make_surface(np.rot90(np.fliplr(img)))



    
 

    
  
    
