import pyautogui
import keyboard
import time
import tkinter as tk
from tkinter import ttk
import webbrowser

class AutoClicker:
    def __init__(self):
        self.running = False
        self.click_positions = []
        self.delay = 0.5  # Adjusted delay to 0.5 seconds between clicks

    def start(self):
        self.running = True
        while self.running:
            for pos in self.click_positions:
                pyautogui.click(pos)
                time.sleep(self.delay)
                if not self.running:
                    break

    def stop(self):
        self.running = False

    def record_click_position(self):
        pos = pyautogui.position()
        self.click_positions.append(pos)

auto_clicker = AutoClicker()

def toggle_auto_clicker(event=None):
    if not auto_clicker.running:
        auto_clicker.record_click_position()
        update_positions_text()
    else:
        auto_clicker.stop()

def start_stop_auto_clicker(event=None):
    if not auto_clicker.running:
        auto_clicker.start()
    else:
        auto_clicker.stop()

def stop_auto_clicker(event=None):
    auto_clicker.stop()

def update_positions_text():
    positions_text.delete(1.0, tk.END)
    for pos in auto_clicker.click_positions:
        positions_text.insert(tk.END, f"({pos[0]}, {pos[1]})\n")

def clear_positions():
    auto_clicker.click_positions = []
    update_positions_text()

# GUI
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("400x400")
root.configure(bg="#FFFFFF")  # Set background color to white

# Style
style = ttk.Style()
style.configure("TFrame", background="#FFFFFF")  # Set frame background color to white

frame = ttk.Frame(root, padding="20")
frame.pack(expand=True, fill=tk.BOTH)

positions_label = ttk.Label(frame, text="Click positions:", font=("Arial", 12))
positions_label.grid(row=0, column=0, pady=5, padx=5)

positions_text = tk.Text(frame, height=10, width=20, font=("Arial", 10))
positions_text.grid(row=1, column=0, pady=5, padx=5)

record_button = ttk.Button(frame, text="Record Position (F)", command=toggle_auto_clicker)
record_button.grid(row=2, column=0, pady=5, padx=5)

start_stop_button = ttk.Button(frame, text="Start/Stop (R)", command=start_stop_auto_clicker)
start_stop_button.grid(row=3, column=0, pady=5, padx=5)

stop_button = ttk.Button(frame, text="Stop (D)", command=stop_auto_clicker)
stop_button.grid(row=4, column=0, pady=5, padx=5)

clear_button = ttk.Button(frame, text="Clear Positions", command=clear_positions)
clear_button.grid(row=5, column=0, pady=5, padx=5)

# Key bindings
keyboard.on_press_key("f", toggle_auto_clicker)
keyboard.on_press_key("r", start_stop_auto_clicker)
keyboard.on_press_key("d", stop_auto_clicker)

# Displaying the acknowledgment with the YouTube link
acknowledgment_label = ttk.Label(root, text="Made by ohsunsett on discord", font=("Arial", 8), foreground="#000000", background="#FFFFFF")
acknowledgment_label.pack(side=tk.BOTTOM, pady=2)

youtube_link_label = ttk.Label(root, text="Visit my YouTube channel", font=("Arial", 8), foreground="#0000FF", background="#FFFFFF", cursor="hand2")
youtube_link_label.bind("<Button-1>", lambda e: webbrowser.open("https://www.youtube.com/@OhSunset"))
youtube_link_label.pack(side=tk.BOTTOM, pady=2)

root.mainloop()
