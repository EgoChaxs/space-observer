from dataclasses import dataclass
from enum import Enum

class ImageSourceType(Enum):
    FILE = "file"
    FOLDER = "folder"

@dataclass
class ImageSensorConfig:
    source_type: ImageSourceType
    path: str