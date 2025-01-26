from RealtimeSTT import AudioToTextRecorder
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
        self.is_listening = False

    def start_listening(self):
        """Start listening in the background."""
        if not self.is_listening:
            self.recorder.start()
            self.is_listening = True

    def stop_listening(self):
        """Stop listening."""
        if self.is_listening:
            self.recorder.stop()
            self.is_listening = False

    def get_last_text(self):
        """Get the last recognized text."""
        text = self.recorder.text()
        return text.lower() if text else ""
