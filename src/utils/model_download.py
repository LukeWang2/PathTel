from ultralytics import YOLO
from constants.constants import Paths


def download_models():
    if not Paths.MODEL_PATH.exists():
        model = YOLO("yolov8n.pt")
        model.save(str(Paths.MODEL_PATH))

    return str(Paths.MODEL_PATH)


if __name__ == "__main__":
    download_models()
