Jarvis Clone - README

1. Install dependencies:
   pip install -r requirements.txt

2. Make sure microphone and speakers are configured.

3. Edit MUSIC_FOLDER in skills/media.py if you want a different music folder.

4. Run:
   python main.py

5. Usage:
   - The assistant listens passively for the wake word "jarvis".
   - Say "Jarvis" then "what's the time", "open youtube", "play music", "take screenshot", "tell me a joke", or "shutdown".
   - You can extend skills by adding functions in skills/ and editing assistant.handle_command.

Notes:
- Speech recognition uses Google's free recognition API (requires internet for recognition). You can change to offline engines if desired.
- pyaudio may need system packages installed first.
