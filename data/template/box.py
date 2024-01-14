from data.base import BaseAnim
import pygame as pg 

class Anim(BaseAnim):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = pg.Surface((100, 100))
        self.box.fill('red')
        self.rect = self.box.get_rect()
        self.pos = [0, 0]


    def update(self, **kwargs):
        surf = kwargs['surf']
        self.pos[0] += 10*kwargs['dt']
        self.rect.topleft  = self.pos
        surf.blit(self.box, self.rect)
