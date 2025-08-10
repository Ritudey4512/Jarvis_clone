# skills/general.py
import webbrowser
import datetime
import pyjokes
import re

GREETINGS = ["hello", "hi", "hey", "good morning", "good evening", "good afternoon"]

def is_greeting(text):
    return any(g in text for g in GREETINGS)

def get_greeting_response():
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        return "Good morning."
    elif hour < 18:
        return "Good afternoon."
    else:
        return "Good evening."

def tell_time():
    now = datetime.datetime.now()
    return now.strftime("The time is %I:%M %p on %A, %B %d, %Y.")

def tell_joke():
    try:
        return pyjokes.get_joke()
    except:
        return "I couldn't find a joke right now."

def extract_website(text):
    # naive extraction
    # e.g. "open youtube" => "youtube.com"
    words = text.split()
    for w in words:
        if "." in w or "youtube" in w or "google" in w:
            return w
    # fallback: look for site name after "open"
    m = re.search(r"open\s+([a-zA-Z0-9\-]+)", text)
    if m:
        return m.group(1) + ".com"
    return None

def open_website(site):
    if not site.startswith("http"):
        site = "https://"+site
    webbrowser.open(site)
