from abc import ABC, abstractmethod

from src.perception.models.observation import Observation
from src.perception.models.detection import Detection


class Detector(ABC):
    """Base interface for object detection implementations."""

    @abstractmethod
    def detect(self, observation: Observation) -> list[Detection]:
        """Detect entities present in an observation.

        Args:
            observation: Input observation containing sensor data.

        Returns:
            List of detections produced from the observation.
        """
        ...