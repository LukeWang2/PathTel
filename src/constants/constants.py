from pathlib import Path

# Get the project root directory (where src, data, etc. are located)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()


class Paths:
    # Directories
    DATA_DIR = PROJECT_ROOT / "data"
    MODELS_DIR = DATA_DIR / "models"
    CONFIGS_DIR = DATA_DIR / "configs"

    # Files
    MODEL_PATH = MODELS_DIR / "yolov8n.pt"
    CONFIG_PATH = CONFIGS_DIR / "settings.yaml"
    LLAVA_PATH = MODELS_DIR / "llava-v1.5-7b-q4.gguf"
    OPENAI_PATH = "gpt-4-vision-preview"

    NAV_MAP = PROJECT_ROOT / "constants" / "nav_map.npy"

    @classmethod
    def ensure_dirs_exist(cls):
        """Create all necessary directories if they don't exist."""
        for directory in [
            cls.DATA_DIR,
            cls.MODELS_DIR,
            cls.CONFIGS_DIR,
            cls.LLAVA_PATH,
            cls.NAV_MAP,
        ]:
            directory.mkdir(parents=True, exist_ok=True)
