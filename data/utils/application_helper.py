from data.utils.wallpaper import WallPaper
import asyncio, tkinter, customtkinter


__all__ = ["AsyncTk", "set_icon", "menu", "left_side"]  

class AsyncTk(tkinter.Tk):
    "Basic Tk with an asyncio-compatible event loop"
    def __init__(self, loop, update_interval):
        super().__init__()
        self.wallpaper = WallPaper()
        self.tasks = []
        self.loop = loop

        self._status = 'working'

        self.after(0, self.__update_asyncio, update_interval)
        self.close_event = asyncio.Event()

    def __update_asyncio(self, interval):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        if self.close_event.is_set():
            self.quit()
        self.after(int(interval * 100), self.__update_asyncio, interval)

    async def status_label_task(self):
        """
        This keeps the Status label updated with an alternating number of dots so that you know the UI isn't
        frozen even when it's not doing anything.
        """
        dots = ''
        while True:
            self.title('Status: %s%s' % (self._status, dots))
            #print(asyncio.all_tasks())
            await asyncio.sleep(1)
            dots += '.'
            if len(dots) >= 6:
                dots = ''

    def initialize(self):
        coros = (
            self.status_label_task(),
            # additional network-bound tasks
        )
        for coro in coros:
            self.tasks.append(self.loop.create_task(coro))

    def on_closing(self, event=0):
        self.close_event.set()
        self.wallpaper.wm.kill_workerw()
        self.destroy()
    


def set_icon(root: tkinter.Tk):
    # file = r'images/logo.png'
    # img = Image.open(file)
    # img.save('images/icon.ico',format = 'ICO', sizes=[(32,32)])
    root.iconbitmap('data/images/icon.ico')

def menu(root: tkinter.Tk):
    menubar = tkinter.Menu(root, background='blue')  
    file = tkinter.Menu(menubar, tearoff=0, foreground='black') 
    file.add_command(label="New")  
    file.add_command(label="Open")  
    file.add_command(label="Save")  
    file.add_command(label="Save as")    
    file.add_separator()  
    file.add_command(label="Exit", command=root.quit)  
    menubar.add_cascade(label="File", menu=file)  

    edit = tkinter.Menu(menubar, tearoff=0)  
    edit.add_command(label="Undo")  
    edit.add_separator()     
    edit.add_command(label="Cut")  
    edit.add_command(label="Copy")  
    edit.add_command(label="Paste")  
    menubar.add_cascade(label="Edit", menu=edit)  

    help = tkinter.Menu(menubar, tearoff=0)  
    help.add_command(label="About", command=root.button_event)  
    menubar.add_cascade(label="Help", menu=help)  

    root.config(menu=menubar)

def left_side(self: tkinter.Tk):
    frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
    frame_left.grid(row=0, column=0, sticky="nswe")

    # configure grid layout (1x11)
    frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
    frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
    frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
    frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

    label_1 = customtkinter.CTkLabel(master=frame_left,
                                            text="Background\nSelections",
                                            text_font=("Roboto Medium", -16))  # font name and size in px
    label_1.grid(row=1, column=0, pady=10, padx=10)


    
    radio_button_1 = customtkinter.CTkRadioButton(master=frame_left, text='Videos'.ljust(11, 'ㅤ') ,
                                                        variable=self.radio_var,
                                                        command=self.change_frame,
                                                        value=0)
    radio_button_1.grid(row=2, column=0, pady=10, padx=20, sticky="nw")

    radio_button_2 = customtkinter.CTkRadioButton(master=frame_left, text='Templates'.ljust(11, 'ㅤ'),
                                                        variable=self.radio_var,
                                                        command=self.change_frame,
                                                        value=1)
    radio_button_2.grid(row=3, column=0, pady=10, padx=20, sticky="nw")

    radio_button_3 = customtkinter.CTkRadioButton(master=frame_left, text='Coming Soon!'.ljust(11, 'ㅤ'),
                                                        variable=self.radio_var,
                                                        command=self.change_frame,
                                                        value=2)
    radio_button_3.grid(row=4, column=0, pady=10, padx=20, sticky="nw")




    customtkinter.CTkLabel(master=frame_left, text="Appearance Mode:").grid(row=9, column=0, pady=0, padx=20, sticky="w")
    optionmenu_1 = customtkinter.CTkOptionMenu(master=frame_left,
                                                    values=["Light", "Dark"],
                                                    command=self.change_appearance_mode)
    optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

    optionmenu_1.set("Dark")




