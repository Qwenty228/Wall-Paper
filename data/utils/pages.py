import customtkinter, os
import tkinter


def right_click_menu(e, c, b: tkinter.Button):
    #print(c.right_click_menu)
    print(e)
    m = tkinter.Menu(c, tearoff=0)
    m.add_command(label="Delete", command=lambda: b.destroy())
    m.tk_popup(e.x_root, e.y_root)


class Page1(customtkinter.CTkFrame):
    def __init__(self, controller,  **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.n_button = 0

        

                

        path = 'data/videos'
        y = customtkinter.CTkButton(master=self, 
                                text='Local Video', text_color='white', width=95, height=85, corner_radius=5,
                                fg_color="gray20", hover_color="gray30", border_color= 'gray10', border_width=3,
                                command=lambda: controller.get_video(y))
        y.grid(row=0, column=0, sticky='ew')
        
        for i, vid in enumerate(os.listdir(path), 1):
            fullpath = os.path.join(path, vid)
            thumb = controller.get_first_frame(fullpath)
            button = customtkinter.CTkButton(master=self, image=thumb, 
                            text=vid.split('.')[0][:10], text_color='white', corner_radius=5, border_width=3,
                            compound="top", fg_color="gray25", hover_color="gray30",  border_color= 'gray10')
            button.grid(row=(i//4), column=(i%4), sticky='ew')
            button.configure(command=lambda btn=button, p=fullpath: controller.button_event(btn, p))
        self.n_button = i + 1
        if (fullpaths := controller.table.get().get('path')) is not None:
            for fp in fullpaths:
                self.add_button(fp)


    def add_button(self, fullpath):
        row = self.n_button//4
        col = self.n_button%4
        thumb = self.controller.get_first_frame(fullpath)

        _, tail = os.path.split(fullpath)

        button = customtkinter.CTkButton(master=self, image=thumb, 
                            text=tail.split('.')[0][:10], text_color='white', corner_radius=5, border_width=3,
                            compound="top", fg_color="gray25", hover_color="gray30",  border_color= 'gray10')
        button.grid(row=row, column=col, sticky='ew')
        button.canvas.bind('<Button-3>', lambda e, c=self.controller, b=button: right_click_menu(e, c, b))
        button.configure(command=lambda btn=button, p=fullpath: self.controller.button_event(btn, p))
        
        
        self.n_button += 1


class Page2(customtkinter.CTkFrame):
    def __init__(self, controller,  **kwargs):
        super().__init__(**kwargs)

class Page3(customtkinter.CTkFrame):
    def __init__(self, controller,  **kwargs):
        super().__init__(**kwargs)