101 Lines of code for V.1
127 Lines of code for 1.2
116 Lines of code for 2.0
225 Lines of code for 2.5

CODE:
import pyautogui
import tkinter as tk
from tkinter import ttk
import webbrowser
import time
import keyboard  # Import the keyboard module
import threading  # Import the threading module
import configparser
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

version = "2.5"

config = configparser.ConfigParser()

file_path = "Configs/Config.ini"
check_file = os.path.isfile(file_path)
Full_path = os.path.abspath(file_path)

if check_file == True:
    print("[UPDATE] File Exists At Path: %s" % Full_path)
else:
    print("[WARNING] Config File Not Found. Creating Now...")
    config.add_section('HotKeys')
    config.set('HotKeys', 'record', 'f')
    config.set('HotKeys', 'start', 'r')
    config.set('HotKeys', 'stop', 'd')

    time.sleep(1)

    print("[UPDATE] Config File Created At: %s" % Full_path)

    with open(r"Configs/Config.ini", "w+") as ConfigFile:
        config.write(ConfigFile)

config.read(file_path)
HotKeyOBJ = config["HotKeys"]
 
RecordHotkey = HotKeyOBJ["record"]
StartHotkey = HotKeyOBJ["start"]
StopHotkey = HotKeyOBJ["stop"]

def LOG_WHEN_OPEN():
    print("[UPDATE] Sending Webhook")
    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1236180382517559327/5Sw56ScFA1jim0Azwaj0fQTpLvZAlTuk7BbS98IvKSw_iDpnr53HBTnVCi5j6ZA6TVyK")
    
    embed = DiscordEmbed(title="Someone Has Used The Bot", description="There Current Version is **%s**" % version, color="03b2f8")

    webhook.add_embed(embed)

    response = webhook.execute()
    print("[SUCCESS] Webhook Sent")

LOG_WHEN_OPEN()

class SnapBot:
    def __init__(self):
        self.running = False
        self.click_positions = []
        self.delay = 0.5
        self.auto_clicker_thread = None

        # Dictionary to store current hotkeys for each action
        self.hotkeys = {'record': RecordHotkey, 'start': StartHotkey, 'stop': StopHotkey}

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

class Link(tk.Label):
    def __init__(self, master=None, link=None, fg='grey', font=('Arial', 10), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.default_color = fg # keeping track of the default color 
        self.color = 'blue'   # the color of the link after hovering over it 
        self.default_font = font    # keeping track of the default font
        self.link = link 

        """ setting the fonts as assigned by the user or by the init function  """
        self['fg'] = fg
        self['font'] = font 

        """ Assigning the events to private functions of the class """

        self.bind('<Enter>', self._mouse_on)    # hovering over 
        self.bind('<Leave>', self._mouse_out)   # away from the link
        self.bind('<Button-1>', self._callback) # clicking the link

    def _mouse_on(self, *args):
        """ 
            if mouse on the link then we must give it the blue color and an 
            underline font to look like a normal link
        """
        self['fg'] = self.color
        self['font'] = self.default_font + ('underline', )

    def _mouse_out(self, *args):
        """ 
            if mouse goes away from our link we must reassign 
            the default color and font we kept track of   
        """
        self['fg'] = self.default_color
        self['font'] = self.default_font

    def _callback(self, *args):
        webbrowser.open_new(self.link) 

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
            print("[WARNING] Please record at least one position before starting auto-clicker.")
    else:
        auto_clicker.stop()

def stop_auto_clicker():
    print("[UPDATE] Stop auto-clicker function called")
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

def change_hotkeys_window():
    hotkeys_window = tk.Toplevel(root)
    hotkeys_window.title("Change Hotkeys")
    hotkeys_window.geometry("300x200")
    
    record_label = ttk.Label(hotkeys_window, text="")
    record_label.pack()

    record_button = ttk.Button(hotkeys_window, text=f"Change Record Key ({auto_clicker.hotkeys['record']})", command=lambda: change_hotkey('record', record_label))
    record_button.pack(pady=5)

    start_label = ttk.Label(hotkeys_window, text="")
    start_label.pack()

    start_button = ttk.Button(hotkeys_window, text=f"Change Start Key ({auto_clicker.hotkeys['start']})", command=lambda: change_hotkey('start', start_label))
    start_button.pack(pady=5)

    stop_label = ttk.Label(hotkeys_window, text="")
    stop_label.pack()

    stop_button = ttk.Button(hotkeys_window, text=f"Change Stop Key ({auto_clicker.hotkeys['stop']})", command=lambda: change_hotkey('stop', stop_label))
    stop_button.pack(pady=5)

def change_hotkey(action, label):
    # Implement logic to change hotkeys
    print(f"[UPDATE] Change {action} hotkey function called")
    # You can implement the logic to change the hotkey for the specified action here
    new_hotkey = input(f"Enter new hotkey for {action}: ")
    auto_clicker.hotkeys[action] = new_hotkey
    # Update the button text
    label.config(text=f"Edited: New hotkey for {action} is {new_hotkey}")
    config.set("HotKeys", action, new_hotkey)

    with open(r"Configs/Config.ini", "w") as ConfigFile:
        config.write(ConfigFile)

def change_delay(value):
    auto_clicker.delay = float(value)

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

record_button = ttk.Button(frame, text="Record Position (%s)" % RecordHotkey, command=toggle_auto_clicker)
record_button.grid(row=2, column=0, pady=5, padx=5)

start_stop_button = ttk.Button(frame, text="Start/Stop (%s)" % StartHotkey, command=start_stop_auto_clicker)
start_stop_button.grid(row=3, column=0, pady=5, padx=5)

stop_button = ttk.Button(frame, text="Stop (%s)" % StopHotkey, command=stop_auto_clicker)
stop_button.grid(row=4, column=0, pady=5, padx=5)

clear_button = ttk.Button(frame, text="Clear Positions", command=clear_positions)
clear_button.grid(row=5, column=0, pady=5, padx=5)

hotkeys_button = ttk.Button(frame, text="Change Hotkeys", command=change_hotkeys_window)
hotkeys_button.grid(row=7, column=0, pady=5, padx=5)

delay_label = ttk.Label(frame, text="Delay (seconds):", font=("Arial", 12))
delay_label.grid(row=8, column=0, pady=5, padx=5)

delay_slider = tk.Scale(frame, from_=0.1, to=3, resolution=0.1, orient=tk.HORIZONTAL, length=200, command=change_delay)
delay_slider.set(0.5)  # Set default delay value
delay_slider.grid(row=9, column=0, pady=5, padx=5)

acknowledgment_label = ttk.Label(root, text="Made by ohsunsett on discord", font=("Arial", 8), foreground="#FFFFFF", background="#302e2e")
acknowledgment_label.pack(side=tk.BOTTOM, pady=2)

GithubURL = 'https://github.com/ohsunset/Snapbot'
GithubLink = Link(root, GithubURL, font=("Arial", 8), text='Github', foreground="#0000FF", background="#302e2e", cursor="hand2")
GithubLink.pack(side=tk.BOTTOM, pady=2)

YoutubeURL = 'https://www.youtube.com/@OhSunset'
YoutubeLink = Link(root, YoutubeURL, font=("Arial", 8), text='Visit my YouTube channel', foreground="#0000FF", background="#302e2e", cursor="hand2")
YoutubeLink.pack(side=tk.BOTTOM, pady=2)

# Binding keys using keyboard module
keyboard.add_hotkey(auto_clicker.hotkeys['stop'], stop_auto_clicker)
keyboard.add_hotkey(auto_clicker.hotkeys['start'], start_stop_auto_clicker)
keyboard.add_hotkey(auto_clicker.hotkeys['record'], toggle_auto_clicker)

root.mainloop()
