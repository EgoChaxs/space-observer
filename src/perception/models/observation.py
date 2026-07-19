from dataclasses import dataclass
from datetime import datetime
import numpy as np

@dataclass(slots=True)
class Observation:
    """
    Represents a single capture produced by a sensor.

    An observation is the immutable output of a sensor at a specific point
    in time. It contains the raw payload and associated metadata, and serves
    as the input to the perception subsystem.

    Attributes:
        id: Unique identifier of the observation.
        sensor_id: Identifier of the sensor that produced the observation.
        timestamp: Time at which the observation was captured.
        payload: Raw sensor data captured by the sensor.
    """
    id: str
    sensor_id: str
    timestamp: datetime
    payload: np.ndarray