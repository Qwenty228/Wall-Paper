import pygame as pg
from pygame import gfxdraw
from random import randint
import numpy as np
from data.base import BaseAnim
from utils.settings import WIDTH, HEIGHT

FIRE_REPS = 10
STEPS_BETWEEN_COLORS = 15
COLORS = ['black', 'aquamarine4', 'aquamarine3', 'aquamarine2',
          'white']
PIXEL_SIZE = 2


class Anim(BaseAnim):
    def __init__(self, **kwargs) -> None:
        self.FIRE_WIDTH = WIDTH//FIRE_REPS
        self.FIRE_HEIGHT = HEIGHT//PIXEL_SIZE
        self.palettes = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surf = pg.Surface(
            [PIXEL_SIZE*self.FIRE_WIDTH, HEIGHT])
        self.dt = 0


    def do_fire(self):
        for x in range(self.FIRE_WIDTH):
            for y in range(1, self.FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    # gradient from white to black uniform
                    # self.fire_array[y-1][x] = color_index - 1
                    # gradient rangom
                    rnd = randint(0, 3)
                    self.fire_array[y-1][(x - rnd + 1) %
                                         self.FIRE_WIDTH] = color_index - rnd % 2
                else:
                    self.fire_array[y-1][x] = 0

    def get_fire_array(self):
        fire_array = np.zeros((self.FIRE_HEIGHT, self.FIRE_WIDTH), dtype=int)

        for i in range(self.FIRE_WIDTH):
            fire_array[self.FIRE_HEIGHT - 1, i] = len(self.palettes) - 1
        return fire_array

    @staticmethod
    def get_palette():
        palette = [(0, 0, 0)]
        for i, color in enumerate(COLORS[:-1]):
            c1, c2 = color, COLORS[i + 1]
            for step in range(STEPS_BETWEEN_COLORS):
                # interpolate c1 color with c2 with how far from c1 the result should look (float 0-1)
                c = pg.Color(c1).lerp(c2, (step + 0.5)/STEPS_BETWEEN_COLORS)
                palette.append(c)
        return palette

    def draw_palette(self, size=50):
        for i, color in enumerate(self.palettes):
            pg.draw.rect(self.app.screen, color, [
                         i * size, self.app.screen.get_height()//2, size - 5, size - 5])

    def draw_fire(self, surf):
        self.fire_surf.fill((0, 0, 0))
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palettes[color_index]
                    gfxdraw.box(self.fire_surf, (x * PIXEL_SIZE,
                                y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE), color)
        for i in range(FIRE_REPS):
            surf.blit(
                self.fire_surf, (self.fire_surf.get_width()*i, 0))
  
    def update(self, **kwargs):
        self.dt += kwargs['dt']
        if self.dt > 0.01: # update fire every 0.01s
            self.dt = 0
            self.do_fire()
        self.draw_fire(kwargs['surf'])


