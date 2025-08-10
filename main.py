# main.py
# Simple launcher that runs the GUI (which runs the assistant)
from gui import JarvisGUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
