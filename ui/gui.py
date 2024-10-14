import tkinter
import tkinter.messagebox
import customtkinter
import os 
from PIL import ImageTk, Image

from .spawner import toggle_engine, PID_FILE

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")

TEMPLATES_DIR = "anim/data/template"
SHADERS_DIR = "anim/data/shaders"
VIDEOS_DIR = "anim/data/videos"

ANIM_FILE = "anim/anim.txt"
def select_animation(anim: str):
    print("Selected animation", anim)
    with open(ANIM_FILE, "w") as f:
        f.write(anim)


def get_thumbnail(directory: str):
    # Open the image file
    img = Image.open(directory)

    # Get the original dimensions of the image
    width, height = img.size

    # Set the desired width, keeping the aspect ratio
    new_width = 200
    new_height = int((new_width / width) * height)

    # Convert to ImageTk format
    return customtkinter.CTkImage(light_image=img, size=(new_width, new_height))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Wallpaper Engine")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Wallpaper", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))
        scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

 
        switch = customtkinter.CTkSwitch(self.sidebar_frame, text="engine switch", command=lambda : toggle_engine())
        switch.grid(row=1, column=0, padx=20, pady=20)
        switch._check_state = os.path.exists(PID_FILE)


        # Page selection buttons
        self.page_buttons = {
            "Templates": self.show_templates,
            "Shaders": self.show_shaders,
            "Videos": self.show_videos,
        }
        button_frame = customtkinter.CTkFrame(self.sidebar_frame)
        button_frame.grid(row=2, column=0, padx=20, pady=(10, 10))
        for i, page_name in enumerate(self.page_buttons.keys(), 0):
            button = customtkinter.CTkButton(button_frame, text=page_name, command=self.page_buttons[page_name])
            button.grid(row=i, column=0, padx=20, pady=(10, 10))


        # Frame to display page content
        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.grid(row=0, column=1,  padx=10, pady=10, sticky="nsew")

        self.show_templates()

        
    def show_templates(self):
        self.clear_content_frame()
        self.display_files_in_frame(TEMPLATES_DIR)

    def show_shaders(self):
        self.clear_content_frame()
        self.display_files_in_frame(SHADERS_DIR)

    def show_videos(self):
        self.clear_content_frame()
        self.display_files_in_frame(VIDEOS_DIR)

    def clear_content_frame(self):
        # Clear the content frame before displaying new content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def display_files_in_frame(self, directory):
        # Get the files in the specified directory and create buttons for them
        base = os.path.split(directory)[1]
        for i, filename in enumerate(os.listdir(directory)):
            if os.path.isfile(os.path.join(directory, filename)) and filename.endswith(".py"):
                name = filename[:-3]
                img = os.path.join("anim/data/images", f"{base}_{name}.png")
                if os.path.exists(img):
                    img = get_thumbnail(img)
                    button = customtkinter.CTkButton(self.content_frame, text=name, width=200, image=img, compound="top")
                else:
                    button = customtkinter.CTkButton(self.content_frame, text=name, width=200)
                x, y = divmod(i, 3)
                button.configure(command=lambda name=name: select_animation(f"{base}.{name}"))
                button.grid(row=x, column=y, padx=40, pady=40)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    print("done")
