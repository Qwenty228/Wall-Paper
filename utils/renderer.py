import pygame as pg
import win32gui, win32con
import moderngl
from typing import Literal
from array import array
import pygame.freetype

from .worker import Worker
from data.base import BaseAnim
from .settings import *



class Renderer:
    def __init__(self, debug, animation: BaseAnim) -> None:
        pg.freetype.init()
        self.animation = animation
        self.wm = Worker()
        self.wm.get_workerw()
        self.mainClock = pg.time.Clock()
        self._clip_surface()
        self.draw_setup()
        self.time = 0
        self.font = pg.freetype.SysFont('Arial', 30)

        self.debug = debug


    def _clip_surface(self):
        win32gui.ShowWindow(self.wm.WorkerW, win32con.SW_MAXIMIZE)
        self.screen = pg.display.set_mode((0, 0), flags=pg.HIDDEN|pg.DOUBLEBUF|pg.OPENGL)
        win32gui.SetParent(pg.display.get_wm_info()['window'], self.wm.WorkerW)
        self.screen = pg.display.set_mode((0, 0), flags=pg.SHOWN|pg.DOUBLEBUF|pg.OPENGL)

    # def pause(self):
    #     self.wm.toggle_workerw_visibility()
        
    def draw_setup(self):
        self.ctx = moderngl.create_context()
        quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0,  1.0, 0.0, 0.0,   # top left
            1.0, 1.0, 1.0, 0.0,     # top right
             -1.0,  -1.0, 0.0, 1.0, # bottom left
             1.0, -1.0, 1.0, 1.0,   # bottom right
        ]))
        self.program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=self.animation.frag_shader)
        self.vao = self.ctx.vertex_array(
            self.program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')]
        )

          
    def surf2tex(self, surf: pg.Surface, mode: Literal['clear', 'image']='image'):
        """Converting pygame Surface to opengl texture"""
        tex = self.ctx.texture(surf.get_size(), 4)  # number of color channels
        if mode != 'clear':
            tex.filter = (moderngl.NEAREST, moderngl.NEAREST)  # no interpolation
            tex.swizzle = 'BGRA'  # gl differs from pygame, so we have to swizzle the colors
            tex.write(surf.get_view('1'))  # write the surface to the texture
        return tex
           



    def animate(self):
        pg.event.pump()
        aspect_ratio = self.screen.get_width()/self.screen.get_height()   
        display = pg.Surface((WIDTH* aspect_ratio, HEIGHT))

        
        while True:
            display.fill('black')
            dt = self.mainClock.tick(FPS)*0.001
            self.time += dt
            img = self.animation.update(surf=display, dt=dt, aspect_ratio=aspect_ratio)
            if img:
                display = img
            if self.debug:
                self.font.render_to(display, (0.5*WIDTH*aspect_ratio, 0), f'FPS: {self.mainClock.get_fps():.2f}', 'white')
                frame_tex = self.surf2tex(display)
            else:
                frame_tex = self.surf2tex(display, self.animation.mode)    
            frame_tex.use(0)
            self.program['tex'] = 0
            self.animation.set_uniforms(self.program, time=self.time, aspect_ratio=aspect_ratio)
            self.vao.render(mode=moderngl.TRIANGLE_STRIP)
        
                

            pg.display.flip()
            frame_tex.release()
            
    