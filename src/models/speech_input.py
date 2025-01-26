# from RealtimeSTT import AudioToTextRecorder
from constants.config import Config


class SpeechInput:
    def __init__(self):
        config = Config()
        speech_settings = config.get_speech_settings()

        self.language = speech_settings.get("language", "en")
        self.recorder = AudioToTextRecorder(
            model="base",
            language=self.language,
        )
        self.is_listening = True
        self.last_text = ""

    def start_listening(self):
        """Start listening for speech input."""
        while True:
            if self.is_listening:
                self.recorder.start()
                self.is_listening = False
                break

    def stop_listening(self):
        """Stop listening."""
        if self.is_listening:
            self.recorder.stop()
            self.is_listening = False

    def get_last_text(self):
        """Get the last recognized text."""
        text = self.recorder.text()
        return text.lower() if text else ""

    def pause_listening(self):
        """Pause listening for speech input."""
        self.is_listening = False
        print("Speech input paused.")

    def resume_listening(self):
        """Resume listening for speech input."""
        self.is_listening = True
        print("Speech input resumed.")
