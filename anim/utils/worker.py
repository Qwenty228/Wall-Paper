import ctypes
import win32con, win32gui, win32api
import logging


# Set DPI awareness
ctypes.windll.user32.SetProcessDPIAware()
# Constants for screen metrics
SM_CXSCREEN = 0
SM_CYSCREEN = 1

WIDTH, HEIGHT =  win32api.GetSystemMetrics(SM_CXSCREEN), win32api.GetSystemMetrics(SM_CYSCREEN)

AREA = WIDTH * HEIGHT

# Function to calculate the intersection area of two rectangles
def rect_intersection(rect1, rect2):
    left = max(rect1[0], rect2[0])
    top = max(rect1[1], rect2[1])
    right = min(rect1[2], rect2[2])
    bottom = min(rect1[3], rect2[3])
    
    # If there's no overlap
    if right < left or bottom < top:
        return 0
    
    # Return the area of the intersection rectangle
    return (right - left) * (bottom - top)

def intersection(hwnd, threshold=0.95):
    name = win32gui.GetWindowText(hwnd).strip()
    if name in ("", "pygame window"): 
        return False


    # Get window rectangle
    window_rect = win32gui.GetWindowRect(hwnd)
    # Calculate intersection area between window and screen
    intersection_area = rect_intersection((0, 0, WIDTH, HEIGHT), window_rect)
    
    # Check if the intersection area is at least 90% of the screen area
    if intersection_area >= threshold * AREA:
        return True
    return False


class Worker:
    def __init__(self) -> None:
        self.WorkerW = None
        self.hidden = False
    
    def is_foreground_window_fullscreen(self):
        """Function to check if the foreground window is fullscreen"""
        # Get the foreground window
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            # Check if the foreground window covers the entire screen
            return intersection(hwnd)
        return False

    def set_workerw(self, hwnd, extra):
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
            self.WorkerW = win32gui.FindWindowEx(0, hwnd, "WorkerW", None)
            if extra and self.WorkerW:
                #pass
                print(f"WorkerW hwnd {hex(self.WorkerW)}")
        

    def get_workerw(self):
        # Obtaining Program Manager Handle
        progman = win32gui.FindWindow('Progman', 'Program Manager')

        # send message to program manager to trigger the creation of worker w
        # a window between desktop icons and the wallpaper
        """
        // Send 0x052C(WM_ERASEBKGND) to Progman. This message directs Progman to spawn a 
        // WorkerW behind the desktop icons. If it is already there, nothing 
        // happens
        """
            # set message to progman
        #print(f"Progman at {hex(progman)}")

        # all the messages below must be sent in the same order for a successfully workerw creation
        # :- https://www.codeproject.com/Articles/856020/Draw-Behind-Desktop-Icons-in-Windows-plus

        win32gui.SendMessageTimeout(progman, 0x052C, 0xD, 1, win32con.SMTO_NORMAL, 1000)
        win32gui.SendMessageTimeout(progman, win32con.WM_ERASEBKGND, 0, 0, win32con.SMTO_NORMAL, 1000)
        win32gui.SendMessageTimeout(
        progman, win32con.WM_ERASEBKGND, 0, 0, win32con.SMTO_NORMAL, 1000
        )
        win32gui.SendMessageTimeout(
            progman, win32con.WM_ERASEBKGND, 0, 0, win32con.SMTO_NORMAL, 1000
        )
        win32gui.SendMessageTimeout(progman, 0x052C, 0xD, 1, win32con.SMTO_NORMAL, 1000)


        win32gui.EnumWindows(self.set_workerw, True)
        

    def kill_workerw(self):
        win32gui.EnumWindows(self.set_workerw, True)
        if self.WorkerW:
            win32gui.SendMessage(self.WorkerW, win32con.WM_CLOSE)

    def hide_workerw(self):
        if not self.hidden:
            win32gui.ShowWindow(self.WorkerW, 0)
            self.hidden = True

    def show_workerw(self):
        if self.hidden:
            self.hidden = False
            win32gui.ShowWindow(self.WorkerW, 1)