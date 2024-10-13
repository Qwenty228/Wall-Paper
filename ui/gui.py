import tkinter
import tkinter.messagebox
import customtkinter
import os
import glob
import pickle
import subprocess
import signal
import ctypes

from data.shaders.fullspectrumcyber import Anim
from data.template.doomfire import Anim as Anim2
# from data.videos.videos import Anim as Anim2

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


def get_animations():
    for file in glob.glob("data/**/*.py", recursive=True):
        if file.endswith("__init__.py") or file.count("\\") == 1:
            continue
        file = file.replace("\\", ".")[:-3]
        yield file


animations = get_animations()

STATE_FILE = "data/process_state.pkl"
COUNTER_FILE = "data/counter.txt"
SCRIPT_FILE = r"ui\background.py"

# Load the saved state from file


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'rb') as f:
            return pickle.load(f)
    return {"running": False, "pid": None}

# Save the current state to file


def save_state(running, pid):
    with open(STATE_FILE, 'wb') as f:
        pickle.dump({"running": running, "pid": pid}, f)

# Read the current counter value from the counter file


def read_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

# Write the counter value to the counter file


def write_counter(value):
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(value))

# Start the subprocess and save its PID


def start_subprocess():
    process = subprocess.Popen(["python", SCRIPT_FILE])
    return process.pid

# Stop the subprocess using the saved PID


def stop_subprocess(pid):
    try:
        os.kill(pid, signal.SIGTERM)  # Send a termination signal
    except ProcessLookupError:
        pass  # If the process doesn't exist, ignore the error

# Check if a process with a given PID is running


def is_process_running(pid):
    PROCESS_QUERY_INFROMATION = 0x1000
    processHandle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFROMATION, 0,pid)
    if processHandle == 0:
        return False
    else:
        ctypes.windll.kernel32.CloseHandle(processHandle)
    return True

def button_callback(app: 'App'):
    if not app.bg_task_state["running"]:
        app.bg_pid = start_subprocess()
        app.bg_task_state["running"] = True
        app.bg_task_state["pid"] = app.bg_pid
    else:
        stop_subprocess(app.bg_task_state["pid"])
        app.bg_task_state["running"] = False
        app.bg_task_state["pid"] = None
    save_state(app.bg_task_state["running"], app.bg_pid)


class App(customtkinter.CTk):
    ind = 0

    def __init__(self, renderer, thread_event):
        super().__init__()

        self.bg_task_state = load_state()
        if self.bg_task_state["running"] and is_process_running(self.bg_task_state["pid"]):
            self.bg_pid = self.bg_task_state["pid"]
        else:
            self.bg_pid = None
            self.bg_task_state["running"] = False

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Wallpaper", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        button = customtkinter.CTkButton(
            self, text="my button", command=lambda: button_callback(self))
        button.grid(row=0, column=0, padx=20, pady=20)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    print("done")
