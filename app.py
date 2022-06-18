from inspect import getmembers, isclass
import tkinter
import tkinter.messagebox
from tkinter import filedialog
import customtkinter
import os
from PIL import Image, ImageTk
import imageio as iio
from data.utils.config import VID_FILE_TYPES
import asyncio


from data.utils.application_helper import *
from data.utils.config import HEIGHT, WIDTH
from data.utils import pages

class App(customtkinter.CTk, AsyncTk):
    WIDTH = WIDTH
    HEIGHT = HEIGHT

    def get_first_frame(self, video):
        if (thumbnail := self._thumbnail.get(video)) is None:
            button_size = (200, 150)
            array = next(iter(iio.get_reader(video, format="FFMPEG")))
            img = Image.fromarray(array)
            ratio = min([l/s for s, l in zip(array.shape[:2], button_size)])
            img = img.resize([int(i*ratio) for i in array.shape[:2][::-1]], Image.ANTIALIAS)
            thumbnail =  ImageTk.PhotoImage(image=img)
            self._thumbnail[video] = thumbnail
        return thumbnail

    

    def __init__(self, loop, update_interval = 1/20):
        super().__init__(loop=loop, update_interval=update_interval)

        self.table = set_up_db()
        self._thumbnail = {}
        self._pages = {}
        self._local = None
        self._prev_local = None
        self.task = None
        self.radio_var = tkinter.IntVar(value=0)
        self.toggle_var = True

 
        customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        set_icon(self)
        
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        
        menu(self)
        # ============ frame_left ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        left_side(self)

        # ============ frame_right ============
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)


        # configure grid layout (3x7)
        self.frame_right.rowconfigure(( 1, 2, 3), weight=1)
        #frame_right.rowconfigure(7, weight=10)
        self.frame_right.rowconfigure(10, minsize=35)
        self.frame_right.columnconfigure(1, weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        customtkinter.CTkLabel(master=self.frame_right, text="select background:").grid(row=0, column=0, pady=0, padx=10)


        switch_1 = customtkinter.CTkSwitch(master=self.frame_right, text='Live Wallpaper ON', variable=tkinter.IntVar(value=1))
        switch_1.grid(row=0, column=1, sticky='ns', pady=5)
        switch_1.configure(command=lambda s=switch_1: self.toggle(s))

        self.set_up_frame()

    def set_up_frame(self):
        classes = getmembers(pages, isclass)
        for i, page in enumerate(classes):
            frame = page[1](controller=self, master=self.frame_right)
            self._pages[i] = frame
            frame.grid(row=1, column=0, columnspan=2, rowspan=4, pady=0, padx=20, sticky="nsew")
            frame.grid_columnconfigure((0,1,2, 3),weight=1)
            frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.change_frame()

     
    def change_frame(self):
        frame = self._pages.get(self.radio_var.get())
        frame.tkraise()


    def get_video(self, button: customtkinter.CTkButton):
        if self._local and button.border_color == 'gray10':
            self.button_event(button, self._local)
            return

        video = filedialog.askopenfilename(title='Select Video or GIF', filetypes=[('files', VID_FILE_TYPES)])
        if video:
            thumb = self.get_first_frame(video)
            button.set_image(thumb)
            button.configure(compound='top')
            self._local = video
            self.button_event(button, self._local)
            
            if str(video) not in self.table.get()['path']:
                self.table.insert(data={"path": str(video)})
                if frame := self._pages.get(0):
                    if self._prev_local:
                        frame.add_button(self._prev_local)

            self._prev_local = video

    def button_event(self, button: customtkinter.CTkButton=None, path=None):
        if path:
            frame = self._pages.get(self.radio_var.get())
            for widget in frame.winfo_children():
                if widget == button:
                    button.configure(border_color='blue')
                else:
                    widget.configure(border_color='gray10')
            
            if self.task:
                self.task.cancel()
                self.taks = None
            self.task = self.loop.create_task(self.wallpaper.draw(self.radio_var.get(), path))


    def toggle(self, switch: customtkinter.CTkSwitch):
        self.toggle_var = switch.check_state
        self.wallpaper.pause()


    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


    async def countint(self):
        while True:
            print('c')
            await asyncio.sleep(2)


if __name__ == "__main__":
    gui = App(asyncio.get_event_loop())
    gui.initialize()
    gui.mainloop()


    # async def main():
    #     app = App()
    #     finish, unfinish = await asyncio.wait([app.run(), clock()], return_when=asyncio.FIRST_COMPLETED)
    
    #asyncio.run(main())