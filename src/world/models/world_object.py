import numpy as np

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class WorldObject:
    """
    Represents a persistent object tracked by the World Model.

    A WorldObject is the World Model's representation of an entity observed
    through perception. Unlike a detection, which only exists within a single
    observation, a WorldObject maintains identity and state across multiple
    observations.

    Attributes:
        id: Unique identifier assigned by the World Model.
        label: Semantic class or name of the object.
        appearance_embedding: Normalized visual feature vector used to compare
            object appearances across observations.
        semantic_location: Current known location or surrounding context of the
            object (for example, "desk" or "table").
        first_seen: Timestamp of the first observation where the object was
            created.
        last_seen: Timestamp of the most recent observation where the object was
            detected.
        confidence: Confidence score representing the current certainty of the
            object's state.
        is_visible: Whether the object was observed in the most recent update.
    """

    id: UUID
    label: str
    appearance_embedding: np.ndarray = field(repr=False)
    semantic_location: UUID | None
    first_seen: datetime
    last_seen: datetime
    confidence: float
    is_visible: bool = True