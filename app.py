import tkinter
import tkinter.messagebox
from tkinter import filedialog
import customtkinter
import os
from PIL import Image, ImageTk
import imageio as iio
from data.utils.config import VID_FILE_TYPES
import asyncio

from data.utils.wallpaper import WallPaper


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
        self.after(int(interval * 1000), self.__update_asyncio, interval)

    async def status_label_task(self):
        """
        This keeps the Status label updated with an alternating number of dots so that you know the UI isn't
        frozen even when it's not doing anything.
        """
        dots = ''
        while True:
            self.title('Status: %s%s' % (self._status, dots))
            #print(asyncio.all_tasks())
            await asyncio.sleep(0.5)
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
        self.destroy()
    

class App(customtkinter.CTk, AsyncTk):
#class App(tkinter.Tk):

    WIDTH = 780
    HEIGHT = 520

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

        self._thumbnail = {}
        self._local = None
        self.task = None

 
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


        self.radio_var = tkinter.IntVar(value=0)

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

        # ============ frame_right ============
        frame_right = customtkinter.CTkFrame(master=self)
        frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)


        # configure grid layout (3x7)
        frame_right.rowconfigure(( 1, 2, 3), weight=1)
        #frame_right.rowconfigure(7, weight=10)
        frame_right.rowconfigure(10, minsize=35)
        frame_right.columnconfigure((1), weight=1)
        frame_right.columnconfigure(2, weight=0)

        customtkinter.CTkLabel(master=frame_right, text="select background:").grid(row=0, column=0, pady=0, padx=10)

        # ============ frame_info ============
        self.frame_info = customtkinter.CTkFrame(master=frame_right)
        self.frame_info.grid(row=1, column=0, columnspan=2, rowspan=4, pady=0, padx=20, sticky="nsew")

        
        # configure grid layout (1x1)
        self.frame_info.grid_columnconfigure((0,1,2, 3),weight=1)
        self.frame_info.grid_rowconfigure((0, 1, 2, 3), weight=1)

        #self.frame_info.columnconfigure(0, weight=1)
        self.change_frame()

   
    def change_frame(self):
        for widget in self.frame_info.winfo_children():
            widget.destroy()
        page = self.radio_var.get()
        if page == 0:
            path = 'data/videos'
            y = customtkinter.CTkButton(master=self.frame_info, 
                                    text='Local Video', text_color='white', width=95, height=85, corner_radius=5,
                                    fg_color="gray20", hover_color="gray30", border_color= 'gray10', border_width=3,
                                    command=lambda: self.get_video(y))
            y.grid(row=0, column=0, sticky='ew')
            for i, vid in enumerate(os.listdir(path), 1):
                fullpath = os.path.join(path, vid)
                thumb = self.get_first_frame(fullpath)
                button = customtkinter.CTkButton(master=self.frame_info, image=thumb, 
                                text=vid.split('.')[0][:10], text_color='white', corner_radius=5, border_width=3,
                                compound="top", fg_color="gray25", hover_color="gray30",  border_color= 'gray10')
                button.grid(row=(i//4), column=(i%4), sticky='ew')
                button.configure(command=lambda btn=button, p=fullpath: self.button_event(btn, p))

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


            

    def button_event(self, button: customtkinter.CTkButton=None, path=None):
        if path:
            for widget in self.frame_info.winfo_children():
                if widget == button:
                    button.configure(border_color='blue')
                else:
                    widget.configure(border_color='gray10')
            
            if self.task:
                self.task.cancel()
            self.task = self.loop.create_task(self.wallpaper.draw(self.radio_var.get(), path))
            


    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


    async def countint(self):
        while True:
            print('c')
            await asyncio.sleep(2)

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




if __name__ == "__main__":
    async def clock():
        i = 0
        while True:
            i +=1 
            print(i)
            await asyncio.sleep(1)
    gui = App(asyncio.get_event_loop())
    gui.initialize()
    gui.mainloop()


    # async def main():
    #     app = App()
    #     finish, unfinish = await asyncio.wait([app.run(), clock()], return_when=asyncio.FIRST_COMPLETED)
    
    #asyncio.run(main())