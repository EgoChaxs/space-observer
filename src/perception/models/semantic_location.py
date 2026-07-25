from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SemanticLocation:
    """
    Represents the semantic location of an observed object.
    The location references another detected object or an environment
    concept within the current observation.

    Attributes
        location_id: Identifier of the object or environment location.
    """

    location_detection_id: str