# skills/media.py
import os
import random
from playsound import playsound
import threading

MUSIC_FOLDER = os.path.expanduser("~/Music")  # default; change as needed

def _find_music_files(folder):
    exts = ('.mp3', '.wav', '.ogg', '.m4a')
    files = []
    for root, _, filenames in os.walk(folder):
        for f in filenames:
            if f.lower().endswith(exts):
                files.append(os.path.join(root, f))
    return files

def play_music_folder():
    files = _find_music_files(MUSIC_FOLDER)
    if not files:
        print("No music found in", MUSIC_FOLDER)
        return
    track = random.choice(files)
    t = threading.Thread(target=playsound, args=(track,), daemon=True)
    t.start()
