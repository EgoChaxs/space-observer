from datetime import datetime
from uuid import uuid4
from pathlib import Path
from PIL import Image
import numpy as np

from src.models.observation import Observation
from src.perception.sensor.sensor import Sensor
from src.perception.sensor.image_config import ImageSensorConfig, ImageSourceType

class ImageSensor(Sensor):
    def __init__(self, config: ImageSensorConfig):
        self.config = config
        self.current_index = 0
        self.images = self._get_images() if config.source_type == ImageSourceType.FOLDER else None
            
    def capture(self) -> Observation:
        payload = self._load_image()

        return Observation(
            id=str(uuid4()),
            sensor_id="image_sensor",
            timestamp=datetime.now(),
            payload=payload,
        )

    def _load_image(self):
        if self.config.source_type == ImageSourceType.FILE:
            return self._load_single_image()

        if self.config.source_type == ImageSourceType.FOLDER:
            return self._load_folder_image()

        raise ValueError(
            f"Unsupported source type: {self.config.source_type}"
        )

    def _load_single_image(self) -> np.ndarray:
        try:
            image = Image.open(self.config.path).convert("RGB")
            return np.array(image)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Image does not exist: {self.config.path}"
            )

    def _load_folder_image(self) -> np.ndarray:
        if self.current_index >= len(self.images):
            raise StopIteration("No more images available")
        
        image = Image.open(self.images[self.current_index]).convert("RGB")

        self.current_index += 1

        return np.array(image)

    def _get_images(self):
        folder = Path(self.config.path)

        extensions = {".jpg", ".jpeg", ".png"}

        return [
            image
            for image in folder.iterdir()
            if image.suffix.lower() in extensions
        ]