import customtkinter, os

class Page1(customtkinter.CTkFrame):
    def __init__(self, controller,  **kwargs):
        super().__init__(**kwargs)
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

class Page2(customtkinter.CTkFrame):
    def __init__(self, controller,  **kwargs):
        super().__init__(**kwargs)

class Page3(customtkinter.CTkFrame):
    def __init__(self, controller,  **kwargs):
        super().__init__(**kwargs)