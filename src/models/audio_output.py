import pyttsx3
import threading


class AudioOutput:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.is_running = False
        self.lock = threading.Lock()  # Lock for thread safety
        self.condition = threading.Condition()  # Condition variable for signaling

    def speak(self, message, speech_input):
        """Convert text to speech in a separate thread."""
        if self.is_running:
            print("Audio output is already running.")
            return  # Prevent starting a new speech if one is already running

        # Pause speech input while speaking
        speech_input.pause_listening()  # Implement this method in SpeechInput

        # Start a new thread for speech
        speech_thread = threading.Thread(
            target=self._speak_thread, args=(message, speech_input)
        )
        speech_thread.start()

    def _speak_thread(self, message, speech_input):
        """Thread target for speaking."""
        with self.lock:
            self.is_running = True
            self.engine.say(message)
            self.engine.runAndWait()  # Wait for the speech to finish
            self.is_running = False

        # Notify that speaking is done
        with self.condition:
            self.condition.notify()  # Notify that TTS has finished

        # Resume speech input after speaking
        speech_input.resume_listening()  # Implement this method in SpeechInput

    def stop(self):
        """Stop the speech engine."""
        self.engine.stop()
