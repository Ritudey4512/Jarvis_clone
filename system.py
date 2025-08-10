# skills/system.py
import pyautogui
import datetime
import os
import platform
import subprocess

def take_screenshot():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = os.path.join(os.getcwd(), f"screenshot_{now}.png")
    img = pyautogui.screenshot()
    img.save(fname)
    return fname

def shutdown():
    os_name = platform.system()
    if os_name == "Windows":
        subprocess.call(["shutdown", "/s", "/t", "5"])
    elif os_name == "Linux":
        subprocess.call(["shutdown", "now"])
    elif os_name == "Darwin":
        subprocess.call(["osascript", "-e", 'tell app "System Events" to shut down'])
    else:
        raise NotImplementedError("Shutdown not implemented for OS: " + os_name)
