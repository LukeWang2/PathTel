from ultralytics import YOLO
from constants.constants import Paths
import os
import requests
from tqdm import tqdm


def download_models():
    if not Paths.MODEL_PATH.exists():
        model = YOLO("yolov8n.pt")
        model.save(str(Paths.MODEL_PATH))

    """Download the LLaVA model if not already present."""
    if not os.path.exists(Paths.LLAVA_PATH):
        os.makedirs("models", exist_ok=True)

        url = "https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/ggml-model-q4_k.gguf"

        print("Downloading LLaVA model...")
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))

        with open(Paths.LLAVA_PATH, "wb") as f, tqdm(
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                pbar.update(size)

    return str(Paths.MODEL_PATH), str(Paths.LLAVA_PATH)


if __name__ == "__main__":
    download_models()
