from dataclasses import dataclass
from enum import Enum


class ImageSourceType(Enum):
    """Supported image source types for image sensors."""

    FILE = "file"
    FOLDER = "folder"


@dataclass(slots=True)
class ImageSensorConfig:
    """Configuration required to initialize an image sensor.

    Attributes:
        sensor_id: Unique identifier for the sensor instance.
        name: Name of the sensor
        source_type: Type of image source used by the sensor.
        path: Path to the image file or folder containing images.
    """
    
    sensor_id: str
    name: str
    source_type: ImageSourceType
    path: str