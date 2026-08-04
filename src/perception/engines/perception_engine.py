from src.perception.models.perception_result import PerceptionResult
from src.perception.models.observation import Observation
from src.perception.models.detection import Detection

from src.perception.sensors.sensor import Sensor
from src.perception.engines.detection_engine import DetectionEngine
from src.perception.builders.evidence_builder import EvidenceBuilder


class PerceptionEngine:
    """
    Coordinates the complete perception pipeline.

    The PerceptionEngine acts as the entry point of the perception subsystem.
    It coordinates sensor input, object detection, and evidence construction
    to transform raw observations into structured perceptual information.

    The engine does not implement perception algorithms itself. Instead, it
    delegates responsibilities to specialized components:

    - Sensor:
        Captures observations from the environment.

    - DetectionEngine:
        Executes object detection and applies detection post-processing.

    - EvidenceBuilder:
        Enriches detections with additional perceptual information and creates
        Evidence representations.

    Pipeline:

        Sensor
          |
          v
        Observation
          |
          v
        DetectionEngine
          |
          v
        Detection[]
          |
          v
        EvidenceBuilder
          |
          v
        Evidence[]
          |
          v
        PerceptionResult

    Attributes:
        sensor:
            Source of observations from the environment.

        detection_engine:
            Executes object detection and returns processed detections.

        evidence_builder:
            Builds enriched Evidence objects from detections.
    """

    def __init__(
        self,
        sensor: Sensor,
        detection_engine: DetectionEngine,
        evidence_builder: EvidenceBuilder
    ):
        """
        Initialize the perception engine.

        Dependencies are injected to keep the engine independent from specific
        implementations. Different sensors, detection engines, or evidence
        builders can be provided without modifying the pipeline logic.

        Args:
            sensor:
                Sensor implementation responsible for capturing observations.

            detection_engine:
                Engine responsible for running object detection and applying
                optional detection post-processing.

            evidence_builder:
                Builder responsible for enriching detections and producing
                Evidence objects.
        """
        self._sensor = sensor
        self._evidence_builder = evidence_builder
        self._detection_engine = detection_engine

    def process(self) -> PerceptionResult:
        """
        Execute a complete perception cycle.

        Captures a new observation, detects objects within that observation,
        enriches detections into Evidence objects, and returns the complete
        perception result.

        Returns:
            PerceptionResult containing the observation and generated evidence
            for detected objects.
        """
        observation = self._observe()
        detections = self._detect(observation)

        evidences = self._evidence_builder.build(
            observation,
            detections
        )

        return PerceptionResult(
            observation=observation,
            evidences=evidences
        )

    def _observe(self) -> Observation:
        """
        Capture an observation from the configured sensor.

        Returns:
            Observation containing the captured sensor data.
        """
        return self._sensor.capture()

    def _detect(self, observation: Observation) -> list[Detection]:
        """
        Detect objects within an observation.

        Args:
            observation:
                Observation containing the sensor payload.

        Returns:
            List of detections produced by the detection engine.
        """
        return self._detection_engine.run(observation)