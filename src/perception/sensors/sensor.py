from abc import ABC, abstractmethod

from perception.models.observation import Observation

class Sensor(ABC):

    @abstractmethod
    def capture(self) -> Observation:
        """Capture a single observation from the sensor."""