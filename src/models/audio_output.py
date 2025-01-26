import threading
from gtts import gTTS
import os
import threading


class AudioOutput:
    def __init__(self):
        self.speech_lock = threading.Lock()
        self.is_speaking = False

    def speak(self, text):
        with self.speech_lock:
            if self.is_speaking:
                print("Speech engine is busy, skipping this request.")
                return False

            self.is_speaking = True

            tts = gTTS(text=text, lang="en", slow=False)
            tts.save("output.mp3")

            os.system("afplay output.mp3")

            self.is_speaking = False
            return True

    def is_busy(self):
        """Check if the audio engine is currently speaking"""
        return self.is_speaking
