from dataclasses import dataclass


@dataclass
class YOLODetectorConfig:
    """Configuration required to initialize a YOLO detector.

    Attributes:
        model_path: Path to the YOLO model weights.
        confidence_threshold: Minimum confidence required for detections.
    """
    model_path: str
    confidence_threshold: float