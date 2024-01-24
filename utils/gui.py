import tkinter
import tkinter.messagebox
import customtkinter
import threading
import glob

from data.shaders.fullspectrumcyber import Anim
from data.template.doomfire import Anim as Anim2
# from data.videos.videos import Anim as Anim2

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



def get_animations():
    for file in glob.glob("data/**/*.py", recursive=True):
        if file.endswith("__init__.py") or file.count("\\") == 1:
            continue
        file = file.replace("\\", ".")[:-3]
        yield file
animations = get_animations()



def button_callback(renderer, thread_event):
    for t in threading.enumerate():
        if t.name == "renderer":
            # print("renderer already running") 
            renderer.on_pause = not renderer.on_pause
            try: 
                anim = next(animations)
                renderer.choose_anim(anim)
            except StopIteration:
                pass
            
            thread_event.set()  # toggle pausing the renderer thread
            return
    # first time start up
    t1 = threading.Thread(target=renderer.animate)
    t1.name = "renderer"
    t1.start()



class App(customtkinter.CTk):
    ind = 0
    def __init__(self, renderer, thread_event):
        super().__init__()
        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")


        button = customtkinter.CTkButton(self, text="my button", command=lambda: button_callback(renderer, thread_event))
        button.grid(row=0, column=0, padx=20, pady=20)



if __name__ == "__main__":
    app = App()
    app.mainloop()
    print("done")