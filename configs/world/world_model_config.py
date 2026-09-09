from dataclasses import dataclass


@dataclass(slots=True)
class WorldModelConfig:
    """
    Configuration for World Model behavior.

    Attributes:
        match_threshold:
            Minimum appearance similarity required to match an observation
            to an existing WorldObject.

        track_timeout_seconds:
            Maximum amount of time a lost object's Track is kept for possible
            re-association before it is removed from the tracking state.
    """

    match_threshold: float = 0.60
    track_timeout_seconds: int = 20