from constants.config import Config
from services.vision_service import VisionService
from services.navigation_service import run_nav
from utils.model_download import download_models
from models.speech_input import SpeechInput
import threading
import time


def process_video(vision_service, stop_event):
    """Process video in a separate thread."""
    print("Starting video processing thread...")
    if not vision_service.is_running:  # Check if vision service is running
            vision_service.start()
    while not stop_event.is_set():
        try:
            vision_service.process_frame()
            time.sleep(3)  # Small delay to prevent CPU overuse
        except Exception as e:
            print(f"Error in video thread: {str(e)}")


def process_audio(speech_input, vision_service, stop_event):
    """Process audio in a separate thread."""
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
            target=process_video, args=(vision_service, stop_event)
        )

        # Start both threads
        # audio_thread.start()
        video_thread.start()

        # Wait for keyboard interrupt
        try:
            while True:
                time.sleep(0.1)
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
        if "audio_thread" in locals() and audio_thread.is_alive():
            audio_thread.join()
        if "video_thread" in locals() and video_thread.is_alive():
            video_thread.join()


if __name__ == "__main__":
    main()
