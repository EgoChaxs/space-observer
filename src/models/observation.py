from dataclasses import dataclass
from datetime import datetime
import numpy as np

@dataclass
class Observation:
    id: str
    sensor_id: str
    timestamp: datetime
    payload: np.ndarray