import pygame as pg



class G:
    def __init__(self) -> None:
        self.display = pg.display.get_surface()
        self.r = 0
        self.g = 0
        self.b = 0

        
    @staticmethod
    def gradientRect( window, left_colour, right_colour, target_rect ):
        """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
        colour_rect = pg.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
        pg.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
        pg.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
        colour_rect = pg.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
        window.blit( colour_rect, target_rect )                                    # paint it

    
    def run(self):
        self.r +=1 
        self.g += 2
        self.b += 3
        G.gradientRect(self.display, [self.r%255, self.g%255, self.b%255], [255, 0, 125], pg.Rect([0, 0, *self.display.get_size()]))