from datetime import datetime
from queue import Queue, Empty
from threading import Thread, Lock
from uuid import uuid4

import cv2
import numpy as np

from src.perception.models.observation import Observation
from src.perception.sensors.sensor import Sensor
from configs.perception.camera_sensor_config import CameraSensorConfig


class CameraSensor(Sensor):
    """Sensor that continuously captures frames from an RTSP camera."""

    def __init__(
        self,
        config: CameraSensorConfig,
        queue_size: int = 5,
    ):
        """
        Initialize the camera sensor.

        Args:
            config: Configuration defining the RTSP source and sensor identity.
            queue_size: Maximum number of frames waiting to be processed.
        """
        self.config = config

        self.cap = cv2.VideoCapture(config.rtsp_address)

        if not self.cap.isOpened():
            raise RuntimeError(
                f"Could not open RTSP stream: {config.rtsp_address}"
            )

        self.frame_queue: Queue[np.ndarray] = Queue(
            maxsize=queue_size
        )

        self._running = True

        self._capture_thread = Thread(
            target=self._capture_frames,
            daemon=True,
        )
        self._capture_thread.start()

    def _capture_frames(self):
        """Continuously capture frames and add them to the frame queue."""
        while self._running:
            ret, frame = self.cap.read()

            if not ret:
                continue

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            if self.frame_queue.full():
                try:
                    self.frame_queue.get_nowait()
                except Empty:
                    pass

            self.frame_queue.put_nowait(frame)

    def capture(self) -> Observation:
        """
        Return the next available camera observation.

        Returns:
            Observation containing an RGB image captured from the camera.

        Raises:
            RuntimeError: If no frame is currently available.
        """
        try:
            frame = self.frame_queue.get(timeout=5)
        except Empty:
            raise RuntimeError(
                "No frame available from the camera."
            )

        return Observation(
            id=uuid4(),
            sensor_id=self.config.sensor_id,
            timestamp=datetime.now(),
            payload=frame,
        )

    def close(self):
        """Stop frame capture and release the camera stream."""
        self._running = False

        self._capture_thread.join(timeout=2)

        self.cap.release()