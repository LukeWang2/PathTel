import cv2


class Camera:
    def __init__(self):
        self.device = cv2.VideoCapture(0)
        self.is_running = False
        if not self.device.isOpened():
            raise IOError("Could not access camera. Please check camera permissions")

    def get_frame(self):
        if not self.is_running:
            self.is_running = True
        ret, frame = self.device.read()
        if ret:
            print("Camera frame captured successfully.")
        else:
            print("Failed to capture camera frame.")
        return frame if ret else None

    def release(self):
        if self.is_running:
            self.device.release()
            self.is_running = False

    def __del__(self):
        self.release()
