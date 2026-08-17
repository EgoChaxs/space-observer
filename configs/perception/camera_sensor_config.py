from dataclasses import dataclass


@dataclass(slots=True)
class CameraSensorConfig:
    """
    Configuration required to initialize a camera sensor.

    Attributes:
        sensor_id: Unique identifier for the sensor instance.
        name: Human-readable name of the sensor.
        rtsp_address: RTSP URL used to access the camera stream.
    """

    sensor_id: str
    name: str
    rtsp_address: str