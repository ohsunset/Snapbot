101 Lines of code for V.1
127 Lines of code for 1.2
116 Lines of code for 2.0



CODE:
import pyautogui
import tkinter as tk
from tkinter import ttk
import webbrowser
import time
import keyboard  # Import the keyboard module
import threading  # Import the threading module

class SnapBot:
    def __init__(self):
        self.running = False
        self.click_positions = []
        self.delay = 0.5
        self.auto_clicker_thread = None

    def start_auto_clicker_thread(self):
        self.auto_clicker_thread = threading.Thread(target=self.start)
        self.auto_clicker_thread.start()

    def start(self):
        self.running = True
        while self.running:
            for pos in self.click_positions:
                pyautogui.moveTo(pos)
                pyautogui.click(pos)
                time.sleep(self.delay)
                if not self.running:
                    break

    def stop(self):
        self.running = False
        if self.auto_clicker_thread and self.auto_clicker_thread.is_alive():
            self.auto_clicker_thread.join()

    def record_click_position(self):
        pos = pyautogui.position()
        self.click_positions.append(pos)

auto_clicker = SnapBot()

def toggle_auto_clicker():
    if not auto_clicker.running:
        auto_clicker.record_click_position()
        update_positions_text()
    else:
        auto_clicker.stop()

def start_stop_auto_clicker():
    if not auto_clicker.running:
        if auto_clicker.click_positions:
            auto_clicker.start_auto_clicker_thread()
        else:
            print("Please record at least one position before starting auto-clicker.")
    else:
        auto_clicker.stop()

def stop_auto_clicker():
    print("Stop auto-clicker function called")
    auto_clicker.stop()

def update_positions_text():
    positions_text.delete(1.0, tk.END)
    for pos in auto_clicker.click_positions:
        positions_text.insert(tk.END, f"({pos[0]}, {pos[1]})\n")

def clear_positions():
    auto_clicker.click_positions = []
    update_positions_text()

def open_github():
    webbrowser.open("https://github.com/ohsunset/Snapbot")

root = tk.Tk()
root.title("SnapBot")
root.geometry("500x600")
root.configure(bg="#302e2e")

style = ttk.Style()
style.configure("TFrame", background="#302e2e")

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

github_button = ttk.Button(frame, text="GitHub", command=open_github)
github_button.grid(row=6, column=0, pady=5, padx=5)

acknowledgment_label = ttk.Label(root, text="Made by ohsunsett on discord", font=("Arial", 8), foreground="#FFFFFF", background="#302e2e")
acknowledgment_label.pack(side=tk.BOTTOM, pady=2)

youtube_link_label = ttk.Label(root, text="Visit my YouTube channel", font=("Arial", 8), foreground="#0000FF", background="#302e2e", cursor="hand2")
youtube_link_label.pack(side=tk.BOTTOM, pady=2)

# Binding keys using keyboard module
keyboard.add_hotkey('d', stop_auto_clicker)
keyboard.add_hotkey('r', start_stop_auto_clicker)
keyboard.add_hotkey('f', toggle_auto_clicker)

root.mainloop()
