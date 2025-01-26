import yaml
from constants.constants import Paths


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        if not Paths.CONFIG_PATH.exists():
            raise FileNotFoundError(
                f"Configuration file not found at {Paths.CONFIG_PATH}"
            )

        with open(Paths.CONFIG_PATH, "r") as f:
            self.settings = yaml.safe_load(f)

    def get_camera_settings(self):
        return self.settings.get("camera", {})

    def get_model_settings(self):
        return self.settings.get("model", {})

    def get_llava_settings(self):
        return self.settings.get("llava", {})

    def get_audio_settings(self):
        return self.settings.get("audio", {})

    def get_navigation_settings(self):
        return self.settings.get("navigation", {})

    def get_speech_settings(self):
        return self.settings.get("speech", {})
