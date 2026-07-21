from dataclasses import dataclass

from src.perception.models.observation import Observation
from src.perception.models.evidence import Evidence

@dataclass(slots=True)
class PerceptionResult:
    """
    Represents the output of the perception subsystem for a single observation.

    Attributes:
        observation: The observation processed by the perception subsystem.
        evidences: The perceptual evidence extracted from the observation.
    """

    observation: Observation
    evidences: list[Evidence]