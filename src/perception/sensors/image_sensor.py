from datetime import datetime
from uuid import uuid4
from pathlib import Path
from PIL import Image
import numpy as np

from src.perception.models.observation import Observation
from src.perception.sensors.sensor import Sensor
from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType

class ImageSensor(Sensor):
    """Sensor implementation that captures observations from image sources.

    Supports both single image files and folders containing multiple images.
    """

    def __init__(self, config: ImageSensorConfig):
        """Initialize the image sensor with its configuration.

        Args:
            config: Configuration defining the image source and sensor identity.
        """
        self.config = config
        self.current_index = 0
        self.images = self._get_images() if config.source_type == ImageSourceType.FOLDER else None
            
    def capture(self) -> Observation:
        """Capture an image and wrap it into an observation.

        Returns:
            Observation containing the captured image data and metadata.
        """
        payload = self._load_image()

        return Observation(
            id=str(uuid4()),
            sensor_id=self.config.sensor_id,
            timestamp=datetime.now(),
            payload=payload,
        )

    def _load_image(self) -> np.ndarray:
        """Load an image depending on the configured source type.

        Returns:
            Loaded image represented as a NumPy array.
        """
        if self.config.source_type == ImageSourceType.FILE:
            return self._load_single_image()

        if self.config.source_type == ImageSourceType.FOLDER:
            return self._load_folder_image()

        raise ValueError(
            f"Unsupported source type: {self.config.source_type}"
        )

    def _load_single_image(self) -> np.ndarray:
        """Load a single image from the configured file path.

        Returns:
            RGB image represented as a NumPy array.
        """
        image = Image.open(self.config.path).convert("RGB")

        return np.array(image)

    def _load_folder_image(self) -> np.ndarray:
        """Load the next image from the configured image folder.

        Returns:
            RGB image represented as a NumPy array.

        Raises:
            StopIteration: If all images in the folder have been consumed.
        """
        if self.current_index >= len(self.images):
            raise StopIteration("No more images available")
        
        image = Image.open(self.images[self.current_index]).convert("RGB")

        self.current_index += 1

        return np.array(image)

    def _get_images(self) -> list[Path]:
        """Retrieve supported image files from the configured folder.

        Returns:
            Sorted list of image paths available in the folder.
        """
        folder = Path(self.config.path)

        extensions = {".jpg", ".jpeg", ".png"}

        return sorted(
            image
            for image in folder.iterdir()
            if image.suffix.lower() in extensions
        )