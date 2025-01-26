from constants.config import Config
from services.vision_service import VisionService
from services.navigation_service import run_nav
from utils.model_download import download_models
from models.speech_input import SpeechInput
import threading
import time
import traceback

# Global variable to track if audio thread is running
video_thread_running = False
audio_thread_running = False
audio_thread_lock = threading.Lock()  # Lock for thread safety
video_thread_lock = threading.Lock()


def process_video(vision_service, speech_input, stop_event):
    """Process video in a separate thread."""
    global video_thread_running

    with video_thread_lock:
        if video_thread_running:
            print("Video thread is already running.")
            return  # Prevent starting the thread again

        video_thread_running = True
        print("Starting video processing thread...")

    vision_service.start()  # Explicitly start the vision service

    while not stop_event.is_set():
        try:
            vision_service.process_frame(speech_input)
            time.sleep(3)  # Small delay to prevent CPU overuse

        except Exception as e:
            print(f"Error in video thread: {e}")
            traceback.print_exc()

    with video_thread_lock:
        video_thread_running = False  # Reset the flag when the thread stops
        print("Video processing thread has stopped.")

    with video_thread_lock:
        video_thread_running = False  # Reset the flag when the thread stops
        print("Video processing thread has stopped.")


def process_audio(speech_input, vision_service, stop_event):
    """Process audio in a separate thread."""
    global audio_thread_running

    with audio_thread_lock:
        if audio_thread_running:
            print("Audio thread is already running.")
            return  # Prevent starting the thread again

        audio_thread_running = True
        print("Starting audio processing thread...")

    speech_input.start_listening()

    while not stop_event.is_set():
        try:
            command = speech_input.get_last_text()
            if command:
                print(f"Received command: {command}")
                vision_service.handle_command(command)
            time.sleep(0.5)  # Small sleep to prevent CPU overuse

        except Exception as e:
            print(f"Error in audio thread: {str(e)}")

    with audio_thread_lock:
        audio_thread_running = False  # Reset the flag when the thread stops
        print("Audio processing thread has stopped.")


def initialize_system():
    """Initialize all required components and models."""
    try:
        # Ensure model is downloaded
        model_path = download_models()
        print(f"Models loaded from: {model_path}")

        # Initialize speech input
        speech_input = SpeechInput()
        print("Speech recognition initialized")

        # Initialize vision service
        vision_service = VisionService()
        print("Vision service initialized")

        return vision_service, speech_input

    except Exception as e:
        print(f"Failed to initialize system: {str(e)}")
        raise


def main():
    print("Starting Indoor Navigation Assistant")
    stop_event = threading.Event()

    try:
        vision_service, speech_input = initialize_system()
        print("System initialized successfully. Starting main loops...")

        # Create threads for audio and video processing
        # audio_thread = threading.Thread(
        #     target=process_audio, args=(speech_input, vision_service, stop_event)
        # )

        video_thread = threading.Thread(
            target=process_video, args=(vision_service, speech_input, stop_event)
        )

        # Start both threads
        # audio_thread.start()
        print("Audio thread started.")
        video_thread.start()
        print("Video thread started.")

        # Wait for keyboard interrupt
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            stop_event.set()

    except Exception as e:
        print(f"Error in main: {str(e)}")
        stop_event.set()

    finally:
        print("Cleaning up resources...")
        stop_event.set()

        # Stop services
        if "speech_input" in locals():
            speech_input.stop_listening()
        if "vision_service" in locals():
            vision_service.stop()

        # Wait for threads to finish
        # if "audio_thread" in locals() and audio_thread.is_alive():
        # audio_thread.join()
        # print("Audio thread joined.")
        if "video_thread" in locals() and video_thread.is_alive():
            video_thread.join()
            print("Video thread joined.")


if __name__ == "__main__":
    main()
