from configs.perception.detection_engine_config import DetectionEngineConfig

from src.perception.models.observation import Observation
from src.perception.models.detection import Detection
from src.perception.detectors.detector import Detector


class DetectionEngine:
    """
    Coordinates the object detection pipeline.

    The detection engine delegates object detection to the configured detector
    and optionally applies post-processing to improve detection quality before
    returning the final results.
    """

    def __init__(self, config: DetectionEngineConfig, detector: Detector):
        """
        Initialize the detection engine.

        Args:
            config: Configuration controlling detection post-processing.
            detector: Detector implementation used to generate detections.
        """
        self._config = config
        self._detector = detector

    def run(self, observation: Observation) -> list[Detection]:
        """
        Run detection on an observation.

        Args:
            observation: Observation containing sensor data.

        Returns:
            List of detections produced by the configured detector.
        """
        detections = self._detector.detect(observation)

        if self._config.enable_post_processing:
            detections = self._post_process(
                observation,
                detections
            )

        return detections

    def _post_process(
        self,
        observation: Observation,
        detections: list[Detection]
    ) -> list[Detection]:
        """
        Apply post-processing operations to raw detections.

        Args:
            observation: Observation from which detections were produced.
            detections: Raw detections returned by the detector.

        Returns:
            Post-processed detections.
        """
        detections = self._filter_by_max_area_ratio(
            observation,
            detections
        )

        return detections

    def _filter_by_min_area_ratio(
        self,
        observation: Observation,
        detections: list[Detection]
    ) -> list[Detection]:
        """
        Remove detections that occupy too little of the image.

        Args:
            observation: Observation containing the source image.
            detections: Detections to filter.

        Returns:
            Filtered detections satisfying the minimum area ratio.
        """
        filtered = []

        for detection in detections:
            ratio = self._compute_area_ratio(observation, detection)

            if ratio >= self._config.min_area_ratio:
                filtered.append(detection)

        return filtered

    def _filter_by_max_area_ratio(
        self,
        observation: Observation,
        detections: list[Detection]
    ) -> list[Detection]:
        """
        Remove detections that occupy too much of the image.

        Args:
            observation: Observation containing the source image.
            detections: Detections to filter.

        Returns:
            Filtered detections satisfying the maximum area ratio.
        """
        filtered = []

        for detection in detections:
            ratio = self._compute_area_ratio(observation, detection)

            if ratio <= self._config.max_area_ratio:
                filtered.append(detection)

        return filtered

    def _compute_area_ratio(
        self,
        observation: Observation,
        detection: Detection
    ) -> float:
        """
        Compute the relative area occupied by a detection.

        The returned value is the ratio between the detection's bounding box
        area and the total image area.

        Args:
            observation: Observation containing the source image.
            detection: Detection whose bounding box is evaluated.

        Returns:
            Bounding box area divided by the image area.
        """
        height, width = observation.payload.shape[:2]

        image_area = width * height

        bbox = detection.bounding_box

        detection_area = (
            (bbox.x2 - bbox.x1)
            *
            (bbox.y2 - bbox.y1)
        )

        ratio = detection_area / image_area

        return ratio