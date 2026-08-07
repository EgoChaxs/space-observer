from src.perception.models.observation import Observation
from src.perception.models.detection import Detection
from src.perception.models.evidence import Evidence

from src.perception.extractors.appearance_extractor import AppearanceExtractor
from src.perception.extractors.semantic_location_extractor import SemanticLocationExtractor


class EvidenceBuilder:
    """
    Builds complete perceptual evidence from object detections.

    The EvidenceBuilder acts as the orchestration layer between raw
    detections and the final evidence representation used by the
    perception subsystem.

    For each detected object, it invokes available extractors to enrich
    the detection with additional perceptual information, such as visual
    appearance embeddings and semantic location.

    The builder does not perform detection itself. It only combines the
    outputs of the detector and extractors into Evidence objects.

    Attributes:
        appearance_extractor: Extracts visual feature representations
            from detected objects.
        semantic_location_extractor: Determines the semantic location
            of detected objects within the observed environment.

    Pipeline position:

        Observation
            |
            v
        Detector
            |
            v
        Detection
            |
            v
        EvidenceBuilder
            |
            +--> AppearanceExtractor
            |
            +--> SemanticLocationExtractor
            |
            v
        Evidence
    """
    def __init__(
            self,
            appearance_extractor: AppearanceExtractor,
            semantic_location_extractor: SemanticLocationExtractor,
    ):
        """
        Initialize the evidence builder.

        Args:
            appearance_extractor:
                Extracts appearance features from detected objects.

            semantic_location_extractor:
                Extracts semantic location information from detected objects.
        """
        
        self._appearance_extractor = appearance_extractor
        self._semantic_location_extractor = semantic_location_extractor

    def build(
            self, 
            observation: Observation, 
            detections: list[Detection]
    ) -> list[Evidence]:
        """
        Build evidence objects for detected entities.

        Each detection is enriched by running the configured extractors.
        The resulting information is aggregated into an Evidence object
        representing everything currently known about that detected object
        from the current observation.

        Args:
            observation:
                The original observation containing the sensor payload used
                by extractors that require access to image data.

            detections:
                List of detections produced by the detector.

        Returns:
            A list of Evidence objects, one for each detection.

        """

        evidences: list[Evidence] = []

        for detection in detections:
            
            embedding = self._appearance_extractor.extract(
                observation,
                detection
            )

            location = self._semantic_location_extractor.extract(
                observation,
                detection,
                detections
            )

            evidence = Evidence(
                detection=detection,
                appearance_embedding=embedding,
                semantic_location=location,
            )

            evidences.append(evidence)

        return evidences