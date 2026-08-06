from dataclasses import dataclass


@dataclass(slots=True)
class RFDETRDetectorConfig:
    """
    Configuration for the RF-DETR detector.

    Attributes:
        model_path: Path to the pretrained RF-DETR model weights.
        confidence_threshold: Minimum confidence required for a detection to be returned.
        device: Device on which to run inference (e.g. "cpu" or "cuda").
    """

    model_path: str
    confidence_threshold: float = 0.3
    device: str = "cpu"