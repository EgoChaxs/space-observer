from dataclasses import dataclass, field

from src.perception.models.detection import Detection
from src.perception.models.appearance_embedding import AppearanceEmbedding
from src.perception.models.semantic_location import SemanticLocation
from src.perception.models.relationship import Relationship


@dataclass(slots=True)
class Evidence:
    """
    Represents the complete perceptual evidence for a single observed object.

    Evidence is the canonical output of the perception subsystem for one
    detected object. It aggregates all information extracted during a single
    observation.

    Attributes:
        detection: The originating object detection.
        appearance_embedding: Visual representation of the object's appearance.
        semantic_location: Semantic location of the object.
        relationships: Semantic relationships with other detected objects.
    """

    detection: Detection
    appearance_embedding: AppearanceEmbedding | None = None
    semantic_location: SemanticLocation | None = None
    relationships: list[Relationship] = field(default_factory=list)