from src.models.observation import Observation
from src.models.detection import Detection
from src.perception.detection.detector import Detector


class DetectionEngine:
    """Coordinates the detection pipeline using a detector implementation."""

    def __init__(self, detector: Detector):
        """Initialize the detection engine.

        Args:
            detector: Detector implementation used to generate detections.
        """
        self.detector = detector

    def run(self, observation: Observation) -> list[Detection]:
        """Run detection on an observation.

        Args:
            observation: Observation containing sensor data.

        Returns:
            List of detections produced by the configured detector.
        """
        return self.detector.detect(observation)