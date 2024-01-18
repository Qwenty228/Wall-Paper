import imageio.v3 as iio
import pygame as pg
import pygame.freetype
from array import array
import moderngl
import numpy as np
import win32gui, win32con
from typing import Literal

from .worker import Worker
from data.base import BaseAnim
from data.shaders.circular import Anim
from .settings import *




class Renderer:
    def __init__(self, debug, animation: BaseAnim, app) -> None:
        pg.freetype.init()
        self.debug = debug
        self.animation = animation
        self.app = app
        self.font = pg.freetype.SysFont('Arial', 30)
        
        self.wm = Worker()
        self.wm.get_workerw()
        
        self.time = 0
        self.running = True
    
        
    def __clip_surface(self):
        win32gui.ShowWindow(self.wm.WorkerW, win32con.SW_MAXIMIZE)
        pg.display.set_mode((0, 0), pg.OPENGL | pg.DOUBLEBUF)
        win32gui.SetParent(pg.display.get_wm_info()['window'], self.wm.WorkerW)

    def surf2tex(self, surf: pg.Surface, ctx: moderngl.Context,  mode: Literal['clear', 'image']='image'):
        tex = ctx.texture(surf.get_size(), 4)  # number of color channels
        if mode != 'clear':
            tex.filter = (moderngl.NEAREST, moderngl.NEAREST)  # no interpolation
            tex.swizzle = 'BGRA'  # gl differs from pygame, so we have to swizzle the colors
            tex.write(surf.get_view('1'))  # write the surface to the texture
        return tex

        

    def animate(self):
        self.__clip_surface()
      

    
        ctx = moderngl.create_context()
        quad_buffer = ctx.buffer(data=array('f', [
            -1.0,  1.0, 0.0, 0.0,   # top left
            1.0, 1.0, 1.0, 0.0,     # top right
            -1.0,  -1.0, 0.0, 1.0,  # bottom left
            1.0, -1.0, 1.0, 1.0,   # bottom right
        ]))

        program = ctx.program(vertex_shader=vert_shader,
                            fragment_shader=self.animation.frag_shader)
        vao = ctx.vertex_array(
            program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')]
        )
        
        clock = pg.time.Clock()
        window = pg.display.get_surface()
        aspect_ratio = window.get_width()/window.get_height()
        display = pg.Surface((WIDTH * aspect_ratio, HEIGHT))

        
        pg.event.pump()
        while self.running:
                display.fill('black')
                dt = clock.tick(FPS)*0.001
                self.time += dt
                img = self.animation.update(surf=display, dt=dt, aspect_ratio=aspect_ratio)
                if img:
                    display = img
                if self.debug:
                    self.font.render_to(display, (0.5*WIDTH*aspect_ratio, 0), f'FPS: {clock.get_fps():.2f}', 'white')
                    frame_tex = self.surf2tex(display, ctx)
                else:
                    frame_tex = self.surf2tex(display, ctx, self.animation.mode)    
                frame_tex.use(0)
                program['tex'] = 0
                self.animation.set_uniforms(program, time=self.time, aspect_ratio=aspect_ratio)
                vao.render(mode=moderngl.TRIANGLE_STRIP)
            
                    

                pg.display.flip()
                frame_tex.release()
                
                

