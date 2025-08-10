# assistant.py
import speech_recognition as sr
import pyttsx3
import threading
import time
from skills import general, media, system

class JarvisAssistant:
    def __init__(self, wake_word="jarvis"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self._configure_tts()
        self.listening = False
        self.stop_listen_flag = threading.Event()

    def _configure_tts(self):
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 10)
        voices = self.engine.getProperty('voices')
        if voices:
            # pick a slightly robotic male/female depending on availability
            self.engine.setProperty('voice', voices[0].id)

    def say(self, text):
        print("JARVIS:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_once(self, timeout=5, phrase_time_limit=7):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = self.recognizer.recognize_google(audio)
                return text.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return ""

    def handle_command(self, text):
        text = text.lower().strip()
        if not text:
            return

        # Remove wake word if present
        if text.startswith(self.wake_word):
            text = text[len(self.wake_word):].strip()

        # General small-talk and utilities
        if general.is_greeting(text):
            self.say(general.get_greeting_response())
            return

        if "time" in text or "date" in text:
            ans = general.tell_time()
            self.say(ans)
            return

        if "open" in text and ("website" in text or "site" in text or "open" in text):
            site = general.extract_website(text)
            if site:
                self.say(f"Opening {site}")
                general.open_website(site)
            else:
                self.say("Which website should I open?")
            return

        if "play music" in text or "play song" in text:
            self.say("Playing music for you.")
            media.play_music_folder()
            return

        if "joke" in text or "tell me a joke" in text:
            self.say(general.tell_joke())
            return

        if "screenshot" in text or "take screenshot" in text:
            fname = system.take_screenshot()
            self.say(f"Screenshot saved to {fname}")
            return

        if "shutdown" in text or "shutdown computer" in text:
            self.say("Are you sure you want to shutdown? Say yes to confirm.")
            confirm = self.listen_once(timeout=4, phrase_time_limit=3)
            if "yes" in confirm:
                self.say("Shutting down system.")
                system.shutdown()
            else:
                self.say("Shutdown cancelled.")
            return

        # Fallback
        self.say("I didn't understand that. I can tell time, open websites, play music, take screenshots, or tell jokes.")

    def run(self):
        self.say("Jarvis activated. Say 'Jarvis' to wake me up.")
        while not self.stop_listen_flag.is_set():
            print("Listening for wake word...")
            text = self.listen_once(timeout=6, phrase_time_limit=4)
            if not text:
                continue
            print("Heard:", text)
            if self.wake_word in text:
                self.say("Yes?")
                # listen for the command
                cmd = self.listen_once(timeout=6, phrase_time_limit=8)
                print("Command:", cmd)
                self.handle_command(cmd)

    def stop(self):
        self.stop_listen_flag.set()
