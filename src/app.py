from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import base64
import os
from models.camera import Camera
import subprocess
from face_recognition.face_detect import store_face, find_face
from models.audio_output import AudioOutput  # Import speak function

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Camera
camera = Camera()

# Directory to save images
UPLOAD_FOLDER = "face_recognition_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_frames():
    """Generates frames from the camera and emits them via WebSocket."""
    while True:
        try:
            frame = camera.get_frame()
            if frame is None or frame.size == 0:
                continue

            face_names = find_face(frame)

            if face_names:
                speak("I see " + ", ".join(face_names))

            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('video_frame', {
                'frame': frame_data,
                'faces': face_names  # Send detected face names
            })
        except Exception as e:
            print(f"Error in generate_frames: {e}")
            continue

        # frame = camera.get_frame()
        # if frame is None or frame.size == 0:
        #     continue

        # _, buffer = cv2.imencode('.jpg', frame)
        # frame_data = base64.b64encode(buffer).decode('utf-8')
        # socketio.emit('video_frame', {'frame': frame_data})
        # time.sleep(0.03)  # Frame rate

@socketio.on('start_stream')
def start_stream():
    """Starts streaming frames to the client."""
    socketio.start_background_task(generate_frames)

@socketio.on('upload_image')
def handle_image(data):
    """
    Handles incoming image data sent via WebSocket.
    Saves the image to the UPLOAD_FOLDER.
    """
    try:
        # Extract the base64 image and file name from the client
        image_data = data.get("image")
        file_name = data.get("name", "image.png")

        # Decode the base64 image and save it to the folder
        image_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_data.split(",")[1]))

        # Acknowledge successful saving
        socketio.emit("upload_response", {"status": "success", "path": image_path})
        print(f"Image saved: {image_path}")

        try:
            store_face(image_path, user_name)
            print(f"Face stored for user: {user_name}")
            socketio.emit("upload_response", {"status": "success", "message": f"Face stored for {user_name}"})
        except Exception as e:
            print(f"Error storing face: {e}")
            socketio.emit("upload_response", {"status": "error", "message": "Face storage failed."})
    except Exception as e:
        print(f"Error saving image: {e}")
        socketio.emit("upload_response", {"status": "error", "message": str(e)})

@app.route('/')
def index():
    return "WebSocket Video Stream"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=4000)

