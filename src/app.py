from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import base64
import time
from models.camera import Camera

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

camera = Camera()  

def generate_frames():
    while True:
        try:
            frame = camera.get_frame()
            if frame is None or frame.size == 0:
                continue

            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            socketio.emit('video_frame', {'frame': frame_data})
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

@app.route('/')
def index():
    return "WebSocket Video Stream"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=4000)
