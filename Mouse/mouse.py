import ctypes
import time
import random
import threading
import tkinter as tk
from tkinter import messagebox

# Configuration
screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

# Global variables
mouse_thread = None
sleep_thread = None
running_event = threading.Event()

def move_mouse(interval):
    while running_event.is_set():
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        ctypes.windll.user32.SetCursorPos(x, y)
        time.sleep(interval)

def prevent_sleep(key_interval):
    while running_event.is_set():
        ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)  # Press SHIFT key
        ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)  # Release SHIFT key
        time.sleep(key_interval)

def start_program():
    global mouse_thread, sleep_thread
    if running_event.is_set():
        messagebox.showinfo("Info", "Program is already running!")
        return

    try:
        interval = float(entry_interval.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid interval.")
        return

    running_event.set()

    mouse_thread = threading.Thread(target=move_mouse, args=(interval,))
    sleep_thread = threading.Thread(target=prevent_sleep, args=(240,))

    mouse_thread.start()
    sleep_thread.start()

def stop_program():
    if running_event.is_set():
        running_event.clear()
        mouse_thread.join()
        sleep_thread.join()
        messagebox.showinfo("Info", "Program stopped.")
    else:
        messagebox.showinfo("Info", "Program is not running.")

# Create the GUI
root = tk.Tk()
root.title("Mouse Mover")

frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

label = tk.Label(frame, text="Interval (seconds):")
label.grid(row=0, column=0)

entry_interval = tk.Entry(frame)
entry_interval.grid(row=0, column=1)
entry_interval.insert(0, "5")  # Default interval

start_button = tk.Button(frame, text="Start", command=start_program, width=10)
start_button.grid(row=1, column=0, pady=10)

stop_button = tk.Button(frame, text="Stop", command=stop_program, width=10)
stop_button.grid(row=1, column=1, pady=10)

root.mainloop()
