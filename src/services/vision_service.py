import cv2
from ultralytics import YOLO
from constants.config import Config
from models.camera import Camera
from models.audio_output import AudioOutput


class VisionService:
    def __init__(self):
        config = Config()
        model_settings = config.get_model_settings()

        self.model = YOLO(model_settings["path"])
        self.confidence_threshold = model_settings["confidence_threshold"]
        self.classes_of_interest = model_settings["classes_of_interest"]
        self.camera = Camera()
        self.audio = AudioOutput()

    def detect_objects(self, frame):
        results = self.model(frame)
        return results

    def process_scene(self, frame):
        # Detect objects, obstacles, and paths
        detections = self.detect_objects(frame)

        # Process results and generate navigation guidance
        guidance = self.generate_guidance(detections)
        return guidance

    def process_frame(self):
        frame = self.camera.get_frame()
        if frame is not None:
            detections = self.detect_objects(frame)
            guidance = self.generate_guidance(detections)
            self.audio.speak(guidance)

    def generate_guidance(self, detections):
        # TODO: Implement guidance generation logic
        ...
