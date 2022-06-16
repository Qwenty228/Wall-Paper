import ctypes
import win32con, win32gui



class Window:
    def __init__(self) -> None:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        self.WorkerW = None
        self.hidden = False


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

    def toggle_workerw_visibility(self):
        self.hidden = not self.hidden  
        win32gui.EnumWindows(self.set_workerw, False)
        if self.hidden:
            win32gui.ShowWindow(self.WorkerW, 1)
        else:
            win32gui.ShowWindow(self.WorkerW, 0)
         
        
