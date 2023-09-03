import tkinter as tk
import pyautogui
from PIL import ImageGrab
import threading
import time
import keyboard
import numpy as np

# Global variables
target_color = (0, 0, 0)
hotkey_combination = ["shift"]  # Default hotkey
color_picking_mode = False
screenshot = None
cursor_smoothness = 50  # Default smoothness level

# Function to capture the screen
def capture_screen():
    global screenshot
    screenshot = np.array(ImageGrab.grab())

# Initial screen capture
capture_screen()

# Function to find the closest location of the target color to the cursor
def find_closest_target_color():
    time.sleep(0.1)  # Sleep for 0.1 seconds (adjust as needed)
    cursor_x, cursor_y = pyautogui.position()
    search_radius = 50  # Adjust this value to limit the search area

    # Define the search area boundaries
    left = max(0, cursor_x - search_radius)
    right = min(screenshot.shape[1], cursor_x + search_radius)
    top = max(0, cursor_y - search_radius)
    bottom = min(screenshot.shape[0], cursor_y + search_radius)

    min_distance = float('inf')
    closest_x, closest_y = None, None

    for x in range(left, right):
        for y in range(top, bottom):
            pixel_color = screenshot[y, x, :3]
            distance = np.linalg.norm(np.array(pixel_color) - np.array(target_color))
            if distance < min_distance:
                min_distance = distance
                closest_x, closest_y = x, y

    return closest_x, closest_y

# Function to set the target color
def set_target_color():
    global target_color
    target_color = (
        int(red_var.get()),
        int(green_var.get()),
        int(blue_var.get())
    )
    status_label.config(text=f"Target color set to {target_color}")

# Function to perform the action when the hotkey is pressed with cursor smoothing
def hotkey_action_smooth():
    capture_screen()  # Refresh the screenshot
    target_x, target_y = find_closest_target_color()

    # Define the number of steps for cursor smoothing
    num_steps = cursor_smoothness
    for i in range(1, num_steps + 1):
        smooth_x = int(target_x * (i / num_steps) + pyautogui.position()[0] * (1 - i / num_steps))
        smooth_y = int(target_y * (i / num_steps) + pyautogui.position()[1] * (1 - i / num_steps))
        pyautogui.moveTo(smooth_x, smooth_y)
        time.sleep(0.01)  # Adjust this sleep time to control the smoothness

    print("Hotkey activated with cursor smoothing")  # Debug line

# Function to listen for the hotkey combination
def hotkey_listener():
    keyboard.add_hotkey("shift", hotkey_action_smooth)
    keyboard.wait('esc')  # Wait for the 'esc' key to exit

# Function to handle color picker button click
def pick_color():
    global color_picking_mode
    color_picking_mode = not color_picking_mode
    if color_picking_mode:
        pick_color_button.config(text="Pick Color (Click Again to Confirm)")
        window.bind("<Button-1>", on_color_picked)  # Bind left mouse click event
    else:
        pick_color_button.config(text="Pick Color")
        window.unbind("<Button-1>")  # Unbind left mouse click event

def on_color_picked(event):
    pixel_color = pyautogui.pixel(event.x_root, event.y_root)
    target_color = pixel_color[:3]  # Get the RGB values
    red_var.set(target_color[0])
    green_var.set(target_color[1])
    blue_var.set(target_color[2])
    status_label.config(text=f"Target color set to {target_color}")
    global color_picking_mode
    color_picking_mode = False  # Disable color picking mode
    pick_color_button.config(text="Pick Color")

# Function to update the cursor smoothness level
def update_smoothness(value):
    global cursor_smoothness
    cursor_smoothness = int(value)
    smoothness_label.config(text=f"Cursor Smoothness: {cursor_smoothness}")

# Create the main window
window = tk.Tk()
window.title("Color Finder")

# Create RGB input fields using StringVar variables
red_var = tk.StringVar()
green_var = tk.StringVar()
blue_var = tk.StringVar()

red_label = tk.Label(window, text="Red:")
red_entry = tk.Entry(window, textvariable=red_var)
green_label = tk.Label(window, text="Green:")
green_entry = tk.Entry(window, textvariable=green_var)
blue_label = tk.Label(window, text="Blue:")
blue_entry = tk.Entry(window, textvariable=blue_var)

# Create Set Color button
set_color_button = tk.Button(window, text="Set Color", command=set_target_color)

# Create color picker button
pick_color_button = tk.Button(window, text="Pick Color", command=pick_color)

# Create status label
status_label = tk.Label(window, text=f"Target color set to {target_color}")

# Create cursor smoothness slider
smoothness_label = tk.Label(window, text=f"Cursor Smoothness: {cursor_smoothness}")
smoothness_slider = tk.Scale(window, from_=1, to=100, orient="horizontal", command=update_smoothness)

# Layout widgets
red_label.grid(row=0, column=0)
red_entry.grid(row=0, column=1)
green_label.grid(row=1, column=0)
green_entry.grid(row=1, column=1)
blue_label.grid(row=2, column=0)
blue_entry.grid(row=2, column=1)
set_color_button.grid(row=3, column=0, columnspan=2)
pick_color_button.grid(row=4, column=0, columnspan=2)
status_label.grid(row=5, column=0, columnspan=2)
smoothness_label.grid(row=6, column=0, columnspan=2)
smoothness_slider.grid(row=7, column=0, columnspan=2)

# Create a thread for the hotkey listener
hotkey_thread = threading.Thread(target=hotkey_listener)
hotkey_thread.daemon = True
hotkey_thread.start()

# Start the GUI main loop
window.mainloop()
