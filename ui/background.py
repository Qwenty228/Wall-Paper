import time
import os

COUNTER_FILE = "anim/data/counter.txt"

# Read the current counter value from the file
def read_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

# Write the counter value to the file
def write_counter(value):
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(value))

# Start counting in the background
def background_task():
    counter = read_counter()
    while True:
        counter += 1
        write_counter(counter)
        time.sleep(1)

if __name__ == "__main__":
    background_task()
