import sys
import subprocess
import os
import signal

ANIM_FILE = "anim/anim.txt"
PID_FILE = r"anim/data/pid.txt"
RENDER_PATH = r"anim\renderer.py"
# Start the background process for counting
def start_engine(animation:str = "", debug: bool = False):
    cmd = [sys.executable, RENDER_PATH]
    if animation:
        cmd.extend(['-a', animation])
    if debug:
        cmd.append('-d')
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(PID_FILE, 'w') as f:
        f.write(str(process.pid))
    print(f"Engine started in the background (PID {process.pid}).")

# Stop the background process
def stop_counter():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        try:
            os.remove(PID_FILE)
            os.kill(pid, signal.SIGINT)
            subprocess.Popen([sys.executable, RENDER_PATH, '-c'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Engine stopped (PID {pid}).")
        except OSError as e:
            if e.errno == 87:
                print("No such process is running.")
            else:
                raise e

    else:
        print("No counter process is running.")



def toggle_engine():
    if os.path.exists(PID_FILE):
        stop_counter()
    else:
        with open(ANIM_FILE, 'r') as f:
            anim = f.read().strip()
        start_engine(animation=anim, debug=True)