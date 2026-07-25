from dataclasses import dataclass


@dataclass(slots=True)
class OpenVocabularyDetectorConfig:
    """Configuration required to initialize an open vocabulary detector.

    Attributes:
        model_path: Path to the detector model weights.
        prompts: Text prompts describing objects to detect.
        confidence_threshold: Minimum confidence required for detections.
    """

    model_path: str
    prompts: list[str]
    confidence_threshold: float