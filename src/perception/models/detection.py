from dataclasses import dataclass


@dataclass
class BoundingBox:
    """Coordinates defining an object's location in an image."""

    x1: float
    y1: float
    x2: float
    y2: float


@dataclass
class Detection:
    """Represents an object detected in an observation.

    Attributes:
        id: Unique identifier for this detection instance.
        entity: Name of the detected object.
        confidence: Confidence score assigned by the detector.
        bounding_box: Location of the detected object in the image.
    """
    
    id: str
    entity: str
    confidence: float
    bounding_box: BoundingBox