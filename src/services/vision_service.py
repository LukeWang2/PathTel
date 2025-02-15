from ultralytics import YOLO
# from llama_cpp import Llama
from PIL import Image
import numpy as np
import torch
from constants.config import Config
from models.camera import Camera
from models.audio_output import AudioOutput
import cv2
import os
from dotenv import load_dotenv
from openai import OpenAI
import io
import base64
import pyttsx3


class VisionService:
    def __init__(self):
        self.is_running = False
        config = Config()
        model_settings = config.get_model_settings()
        llava_settings = config.get_llava_settings()

        # Initialize YOLO for object detection
        self.model_yolo = YOLO(model_settings["path"])
        self.confidence_threshold = model_settings["confidence_threshold"]
        self.classes_of_interest = model_settings["classes_of_interest"]

        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.camera = None  # Initialize camera when needed
        self.audio = AudioOutput()
        self.current_command = None
        self.frame_count = 0
        self.known_objects = {}
        self.completed = True

    def start(self):
        """Initialize camera if not already running."""
        if not self.is_running:
            self.camera = Camera()
            self.is_running = True

    def stop(self):
        """Clean up resources."""
        if self.is_running:
            if self.camera:
                self.camera.release()
                self.camera = None
            self.is_running = False

    def detect_objects(self, frame):
        """Detect objects in frame using YOLO."""
        results = self.model_yolo(frame)
        return results

    def estimate_distance(self, bbox):
        """Estimate rough distance based on bounding box size."""
        bbox_height = bbox[3] - bbox[1]
        frame_height = self.camera.get_frame().shape[0]
        relative_size = bbox_height / frame_height
        return 1 / relative_size if relative_size > 0 else float("inf")

    def get_object_direction(self, box, frame_width):
        """Get direction of object relative to camera center."""
        center_x = (box[0] + box[2]) / 2

        if center_x < frame_width / 3:
            return "to your left"
        elif center_x > 2 * frame_width / 3:
            return "to your right"
        else:
            return "straight ahead"

    def update_object_tracking(self, detections, frame):
        """Update known object positions and track their movement."""
        frame_width = frame.shape[1]
        current_objects = {}

        for detection in detections:
            for det in detection.boxes.data:
                cls = int(det[5])
                conf = float(det[4])
                box = det[:4].cpu().numpy()  # [x1, y1, x2, y2]

                if conf > self.confidence_threshold:
                    object_type = self.model_yolo.names[cls]
                    if object_type in self.classes_of_interest:
                        distance = self.estimate_distance(box)
                        direction = self.get_object_direction(box, frame_width)

                        if object_type not in current_objects:
                            current_objects[object_type] = []
                        current_objects[object_type].append(
                            (self.frame_count, direction, distance, conf)
                        )

        # Update known objects
        self.known_objects = current_objects
        self.frame_count += 1

    def generate_llava_prompt(self, command=None):
        """Generate a prompt for LLaVA based on the current command."""
        if command:
            return f"""You are an indoor navigation assistant helping a user navigate. 
            Based on the image, {command}
            Provide clear, concise directions using landmarks and spatial references.
            Make it a short sentence that is maximum 2 sentences.
            Focus on safety and clear navigation instructions.
            Describe the scene and suggest the best path forward."""
        else:
            return """You are an indoor navigation assistant. 
            Provide clear, concise directions using landmarks and spatial references.
            Make it a short sentence that is maximum 2 sentences.
            Focus on important landmarks, obstacles, and potential paths.
            Keep the description clear and concise, prioritizing safety and navigation."""

    def get_llava_guidance(self, frame, command=None):
        """Get navigation guidance from LLaVA."""
        try:
            prompt=self.generate_llava_prompt()
            # Convert OpenCV frame (BGR) to PIL Image (RGB)
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            # Save the PIL image to a BytesIO object
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            
            # Encode the bytes as a Base64 string
            base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            print(response.choices[0].message.content)

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error getting LLaVA guidance: {str(e)}")
            return None

    def process_frame(self):
        """Process a single frame from the camera."""
        # Skip frame processing if audio is speaking
        if self.audio.is_busy():
            return

        if not self.is_running:
            self.start()
        print(self.completed)
        if not self.completed:
            return
        
        self.completed = False
        

        frame = self.camera.get_frame()
        if frame is not None:
            # Get YOLO detections
            detections = self.detect_objects(frame)

            # Update object tracking
            self.update_object_tracking(detections, frame)

            # Get LLaVA guidance
            guidance = self.get_llava_guidance(frame, self.current_command)

            if guidance:
                # Check for immediate obstacles
                warnings = []
                for obj_type, detections in self.known_objects.items():
                    for detection in detections:
                        _, direction, distance, _ = detection
                        if distance < 2.0:  # Warning threshold
                            warnings.append(
                                f"Warning: {obj_type} {direction}, {distance:.1f} meters"
                            )

                # Combine warnings with LLaVA guidance
                if warnings:
                    guidance = "; ".join(warnings) + ". " + guidance
                self.audio.speak(guidance)
                self.current_command = None
                self.completed = True


    def handle_command(self, command):
        """Handle voice commands."""
        self.current_command = command.lower()

    def __del__(self):
        if hasattr(self, "is_running") and self.is_running:
            self.stop()
