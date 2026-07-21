from dataclasses import dataclass
from enum import Enum, auto


class RelationshipType(Enum):
    """
    Defines the semantic relationship between two observed objects.
    """

    ON = auto()
    IN = auto()
    NEXT_TO = auto()
    LEFT_OF = auto()
    RIGHT_OF = auto()
    IN_FRONT_OF = auto()
    BEHIND = auto()
    CONNECTED_TO = auto()


@dataclass(slots=True, frozen=True)
class Relationship:
    """
    Represents a semantic relationship between two observed objects.

    Attributes:
        target_id: Identifier of the related object.
        type: Type of relationship with the target object.
    """

    target_detection_id: str
    type: RelationshipType