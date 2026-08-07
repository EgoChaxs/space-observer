from dataclasses import dataclass


@dataclass(slots=True)
class WorldModelConfig:
    """
    Configuration for World Model behavior.
    
    Attributes:
        match_threshold: Minimum appearance similarity required to match an observation to an existing WorldObject.
    """

    match_threshold: float = 0.60