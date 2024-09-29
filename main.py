# main.py

import asyncio
import setBrightness as sb
import time
import tkinter as tk
import threading
import screen_brightness_control as sbc

started = False
ver = "0.0.1"

start_button = None
stop_button = None
brightness_label = None
brightness_slider = None

# Function to run setBrightness.start() asynchronously
async def run_brightness():
    await sb.start()

# Wrapper function to run asyncio tasks in a separate thread
def start_brightness():
    asyncio.run(run_brightness())

# Wrapper function to run asyncio tasks in a separate thread
def stop_brightness():
    asyncio.run(sb.stop())

# Start action - starts the brightness thread
def start_action():
    global started, start_button, stop_button, brightness_slider
    if not started:
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        brightness_slider.config(state=tk.DISABLED)
        started = True
        threading.Thread(target=start_brightness, daemon=True).start()

# Stop action - stops the brightness thread
def stop_action():
    global started, start_button, stop_button
    if started:
        stop_button.config(state=tk.DISABLED)
        start_button.config(state=tk.NORMAL)
        brightness_slider.config(state=tk.NORMAL)
        started = False
        threading.Thread(target=stop_brightness, daemon=True).start()

# Function to regularly update the current brightness setting
def update_brightness_label():
    global brightness_label
    current_brightness = sb.get_current_setting()  # Get current brightness setting
    screen_brightness = sbc.get_brightness()[0]
    brightness_label.config(text=f"Current Brightness: {current_brightness} ({screen_brightness}%)")
    
    brightness_label.after(3000, update_brightness_label)  # Update every 3000 ms (3 seconds)

# Function to update brightness when the slider value is changed
def update_brightness_slider(value):
    brightness_value = int(value)
    sb.force_set(brightness_value)  # Force set the brightness value immediately

def run():
    global start_button, stop_button, brightness_label, brightness_slider
    root = tk.Tk()
    root.title(f"mmt - {ver}")
    root.geometry("300x400")
    root.resizable(False, False)

    start_button = tk.Button(root, text="Start", command=start_action)
    stop_button = tk.Button(root, text="Stop", command=stop_action, state=tk.DISABLED)
    start_button.pack(pady=10)
    stop_button.pack(pady=10)

    monitors = sb.get_monitors_friendly()
    monitor_list = tk.Listbox(root, selectmode=tk.SINGLE)
    for i, monitor in enumerate(monitors):
        monitor_list.insert(i, monitor)
    monitor_list.pack(pady=10, fill=tk.X)

    brightness_label = tk.Label(root, text="Current Brightness: N/A")
    brightness_label.pack(pady=10)

    brightness_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_brightness_slider)
    brightness_slider.pack(pady=10, fill=tk.X)
    brightness_slider.set(sbc.get_brightness()[0])

    update_brightness_label()  # Start the loop to regularly update the brightness label
    root.mainloop()

if __name__ == "__main__":
    run()
