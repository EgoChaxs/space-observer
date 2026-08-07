from configs.perception.open_vocabulary_detector_config import OpenVocabularyDetectorConfig
from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType
from configs.perception.appearance_extractor_config import AppearanceExtractorConfig
from configs.perception.detection_engine_config import DetectionEngineConfig

from src.perception.detectors.open_vocabulary_detector import OpenVocabularyDetector
from src.perception.sensors.image_sensor import ImageSensor
from src.perception.extractors.appearance_extractor import AppearanceExtractor
from src.perception.extractors.semantic_location_extractor import SemanticLocationExtractor
from src.perception.builders.evidence_builder import EvidenceBuilder
from src.perception.engines.detection_engine import DetectionEngine
from src.perception.engines.perception_engine import PerceptionEngine


def main():

    sensor_config = ImageSensorConfig(
        sensor_id="test_dataset",
        source_type=ImageSourceType.FILE,
        path="assets/test_images/img1.jpg"
    )

    sensor = ImageSensor(sensor_config)

    detector_config = OpenVocabularyDetectorConfig(
            model_path="assets/models/grounding_dino",
            prompts=[
                "a desk",
                "a keyboard",
                "a computer mouse",
                "a monitor",
                "headphones",
                "a mug",
                "a backpack"
            ],
            confidence_threshold=0.5
        )
    
    detector = OpenVocabularyDetector(detector_config)

    appearance_extractor_config = AppearanceExtractorConfig(
        model_path="assets/models/dinov3"
    )

    detection_engine_config = DetectionEngineConfig()

    appearance_extractor = AppearanceExtractor(appearance_extractor_config)
    location_extractor = SemanticLocationExtractor()

    evidence_builder = EvidenceBuilder(appearance_extractor, location_extractor)
    detection_engine = DetectionEngine(detection_engine_config, detector)

    perception_engine = PerceptionEngine(sensor, detection_engine, evidence_builder)

    perception_results = perception_engine.process()

    for evidence in perception_results.evidences:
        detection = evidence.detection
        print(
            detection.entity,
            detection.confidence,
            detection.bounding_box
        )

if __name__ == "__main__":
    main()