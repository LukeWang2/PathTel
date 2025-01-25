import cv2


class Camera:
    def __init__(self):
        self.device = cv2.VideoCapture(0)
        if not self.device.isOpened():
            raise IOError("Could not access camera. Please check camera permissions")

    def get_frame(self):
        ret, frame = self.device.read()
        return frame if ret else None
