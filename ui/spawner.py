import sys
import subprocess
import os
import signal





PID_FILE = r"anim/data/pid.txt"
RENDER_PATH = r"anim\renderer.py"
# Start the background process for counting
def start_engine():
    process = subprocess.Popen([sys.executable, RENDER_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
            print(f"Engine stopped (PID {pid}).")
        except ProcessLookupError:
            print("No such process is running.")
    else:
        print("No counter process is running.")


def toggle_engine():
    if os.path.exists(PID_FILE):
        stop_counter()
    else:
        start_engine()