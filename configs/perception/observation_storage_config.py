from dataclasses import dataclass


@dataclass
class ObservationStorageConfig:
    """Configuration settings for managing observation data storage.

    Attributes:
        base_path: The directory path where sensor frames
            will be stored. Defaults to "data/observations".
    """

    base_path: str = "data/observations"