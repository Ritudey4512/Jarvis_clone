# gui.py
import tkinter as tk
from tkinter import ttk
import threading
import time
from assistant import JarvisAssistant

class JarvisGUI:
    def __init__(self, master):
        self.master = master
        master.title("Jarvis Clone")
        master.geometry("520x320")
        master.configure(bg="#0b0f14")

        # header with glowing effect
        self.header = tk.Label(master, text="J A R V I S", font=("Helvetica", 32, "bold"), fg="#00ffea", bg="#0b0f14")
        self.header.pack(pady=12)

        self.status = tk.Label(master, text="Status: Idle", font=("Helvetica", 12), fg="#9ee5db", bg="#0b0f14")
        self.status.pack()

        self.log = tk.Text(master, height=10, bg="#071019", fg="#c7fff0", insertbackground="#c7fff0")
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

        # control buttons
        frame = tk.Frame(master, bg="#0b0f14")
        frame.pack(pady=6)
        self.start_btn = tk.Button(frame, text="Start Assistant", command=self.start_assistant, width=15)
        self.start_btn.pack(side="left", padx=6)
        self.stop_btn = tk.Button(frame, text="Stop Assistant", command=self.stop_assistant, width=15, state="disabled")
        self.stop_btn.pack(side="left", padx=6)

        self.assistant_thread = None
        self.assistant = JarvisAssistant()

        # animate header
        self.glow = 0
        self._animate_header()

    def _animate_header(self):
        # simple pulsing
        color_value = int((1 + (0.5 * (1 + __import__('math').sin(time.time()*2)))) * 100)
        color_value = max(0, min(255, color_value))
        hexc = f'#{0:02x}{color_value:02x}{200:02x}'
        self.header.config(fg=hexc)
        self.master.after(80, self._animate_header)

    def log_message(self, text):
        self.log.insert("end", text + "\n")
        self.log.see("end")

    def start_assistant(self):
        if self.assistant_thread and self.assistant_thread.is_alive():
            return
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status.config(text="Status: Listening for wake word...")
        def run():
            try:
                self.assistant.say = self._say_and_log  # override to log in GUI
                self.assistant.run()
            except Exception as e:
                self.log_message("Assistant error: " + str(e))
        self.assistant_thread = threading.Thread(target=run, daemon=True)
        self.assistant_thread.start()

    def stop_assistant(self):
        self.assistant.stop()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status.config(text="Status: Stopped")
        self.log_message("Assistant stopped.")

    def _say_and_log(self, text):
        self.log_message("JARVIS: " + text)
        # call original tts
        self.assistant.engine.say(text)
        self.assistant.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()
