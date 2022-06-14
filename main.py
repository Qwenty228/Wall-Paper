import numpy
import win32con, win32gui
import pygame as pg
import ctypes

WorkerW = None
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

def set_workerw(hwnd, extra):
    global WorkerW
    """Set the hwnd of correct WorkerW instance."""
    # get correct WorkerW window
    # // 0x00010190 "" WorkerW
    # //   ...
    # //   0x000100EE "" SHELLDLL_DefView
    # //     0x000100F0 "FolderView" SysListView32
    # // 0x00100B8A "" WorkerW       <-- This is the WorkerW instance we are after!
    # // 0x000100EC "Program Manager"
    desktop_icons = win32gui.FindWindowEx(hwnd, 0, "SHELLDLL_DefView", None)
    if desktop_icons:
        #print(f"SHELLDLL_DefView found at {hex(desktop_icons)}")
        WorkerW = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)
        if extra and WorkerW:
            print(f"WorkerW hwnd {hex(WorkerW)}")
       

def get_workerw():
    # Obtaining Program Manager Handle
    progman = win32gui.FindWindow('Progman', 'Program Manager')
    #print(progman)

    # send message to program manager to trigger the creation of worker w
    # a window between desktop icons and the wallpaper
    """
    // Send 0x052C(WM_ERASEBKGND) to Progman. This message directs Progman to spawn a 
    // WorkerW behind the desktop icons. If it is already there, nothing 
    // happens
    """
        # set message to progman
    print(f"Progman at {hex(progman)}")

    # all the messages below must be sent in the same order for a successfully workerw creation
    # this method :- https://www.codeproject.com/Articles/856020/Draw-Behind-Desktop-Icons-in-Windows-plus
    # no longer works on win 11
    # below is the only working way
    win32gui.SendMessageTimeout(progman, 0x052C, 0xD, 1, win32con.SMTO_NORMAL, 1000)
    win32gui.SendMessageTimeout(
        progman, win32con.WM_ERASEBKGND, 0, 0, win32con.SMTO_NORMAL, 1000
    )
    win32gui.SendMessageTimeout(
        progman, win32con.WM_ERASEBKGND, 0, 0, win32con.SMTO_NORMAL, 1000
    )
    win32gui.SendMessageTimeout(
        progman, win32con.WM_ERASEBKGND, 0, 0, win32con.SMTO_NORMAL, 1000
    )
    win32gui.SendMessageTimeout(progman, 0x052C, 0xD, 1, win32con.SMTO_NORMAL, 1000)

    win32gui.EnumWindows(set_workerw, True)
    
    # obtain handle to newly created window

    """// Spy++ output
    // .....
    // 0x00010190 "" WorkerW
    //   ...
    //   0x000100EE "" SHELLDLL_DefView
    //     0x000100F0 "FolderView" SysListView32
    // 0x00100B8A "" WorkerW       <-- This is the WorkerW instance we are after!
    // 0x000100EC "Program Manager" Progman"""

    """
    // We enumerate all Windows, until we find one, that has the SHELLDLL_DefView 
    // as a child. 
    // If we found that window, we take its next sibling and assign it to workerw.
    """
    # wlist = dict()
    # win32gui.EnumWindows(lambda hwnd, result_list:wlist.update({hwnd: win32gui.GetWindowText(hwnd)}), None)

    # for tophandle, topparamhandle in wlist.items():
    #     desktop_icons = win32gui.FindWindowEx(tophandle, 0, "SHELLDLL_DefView", None)
    #     if desktop_icons:
    #         # gets the worker w window after the current one.
    #         workerw = win32gui.FindWindowEx(0, tophandle, 'WorkerW', None)

    #         return workerw

def _kill_workerw():
    win32gui.EnumWindows(set_workerw, True)
    if WorkerW:
        win32gui.SendMessage(WorkerW, win32con.WM_CLOSE)

def toggle_workerw_visibility(hidden):
    win32gui.EnumWindows(set_workerw, False)
    if hidden:
        win32gui.ShowWindow(WorkerW, 1)
        hidden = False
    else:
        win32gui.ShowWindow(WorkerW, 0)
        hidden = True



get_workerw()

win32gui.ShowWindow(WorkerW, win32con.SW_MAXIMIZE)

print(win32gui.GetWindowRect(WorkerW))


screen = pg.display.set_mode((0, 0), flags=pg.HIDDEN|pg.SRCALPHA, vsync=1)
win32gui.SetParent(pg.display.get_wm_info()['window'], WorkerW)
screen = pg.display.set_mode((0, 0), flags=pg.SHOWN|pg.SRCALPHA, vsync=1)


#surface = pg.Surface(pg.display.get_window_size(), pg.SRCALPHA)

Clock = pg.time.Clock()

def gradientRect( window, left_colour, right_colour, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pg.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pg.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pg.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pg.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )                                    # paint it


#gradientRect(screen, (i%255, (2*i)%255, (3*i)%255), ((3*i)%255, (2*i)%255, i%255), pg.Rect(win32gui.GetWindowRect(WorkerW)) )
 

from test import get_frame


running = True
frame = get_frame()

first_frame  = next(frame)

ratio = max([l/s for s, l in zip(first_frame.shape[:2], pg.display.get_window_size())])

new_size = [i*ratio for i in first_frame.shape[:2]]

offset = ((numpy.fromiter(pg.display.get_window_size(), dtype=int) - numpy.fromiter(new_size, dtype=int) )//2).tolist()

print(offset)

while running:
    try:
        Clock.tick(60)
        pg.event.pump()

        image = pg.surfarray.make_surface(next(frame))
        image = pg.transform.scale(image, new_size)
        screen.blit(image, offset)
        pg.display.flip()
    except:
        running = False

_kill_workerw()
    
print('quit')
quit()
    
