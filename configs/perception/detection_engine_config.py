from dataclasses import dataclass


@dataclass(slots=True)
class DetectionEngineConfig:
    """
    Configuration controlling detection post-processing.

    Post-processing is applied after the detector produces raw detections and
    can be used to discard detections that do not satisfy simple geometric
    constraints. This provides a lightweight way to reduce obvious false
    positives before evidence extraction.

    Attributes:
        enable_post_processing: Whether detection post-processing is enabled.
        min_area_ratio: Minimum allowed detection area relative to the image.
            Detections smaller than this ratio are discarded.
        max_area_ratio: Maximum allowed detection area relative to the image.
            Detections larger than this ratio are discarded.
    """

    enable_post_processing: bool = False
    min_area_ratio: float = 0.001
    max_area_ratio: float = 0.5