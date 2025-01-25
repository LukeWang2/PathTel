from constants.config import Config
from services.vision_service import VisionService
from utils.model_download import download_models


def initialize_system():
    """Initialize all required components and models."""
    try:
        # Ensure model is downloaded
        model_path = download_models()
        print(f"Model loaded from: {model_path}")

        # Initialize vision service
        vision_service = VisionService()
        return vision_service

    except Exception as e:
        print(f"Failed to initialize system: {str(e)}")
        raise


def main():
    print("Starting Indoor Navigation Assistant")

    try:
        vision_service = initialize_system()
        print("System initialized successfully. Starting main loop...")

        while True:
            try:
                # Process a single frame
                vision_service.process_frame()

            except KeyboardInterrupt:
                print("Shutting down...")
                break

            except Exception as e:
                print(f"Error in main loop: {str(e)}")
                continue

    finally:
        print("Cleaning up resources...")
        if "vision_service" in locals():
            del vision_service


if __name__ == "__main__":
    main()
