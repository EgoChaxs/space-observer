from configs.perception.open_vocabulary_detector_config import OpenVocabularyDetectorConfig
from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType
from src.perception.detectors.open_vocabulary_detector import OpenVocabularyDetector
from src.perception.sensors.image_sensor import ImageSensor
from src.perception.extractors.appearance_extractor import AppearanceExtractor
from src.perception.extractors.semantic_location_extractor import SemanticLocationExtractor
from src.perception.builders.evidence_builder import EvidenceBuilder
from src.perception.engines.perception_engine import PerceptionEngine
from src.world.world_model import WorldModel


def main():

    sensor_config = ImageSensorConfig(
        sensor_id="test_dataset",
        source_type=ImageSourceType.FOLDER,
        path="assets/test_images/"
    )

    sensor = ImageSensor(sensor_config)

    detector_config = OpenVocabularyDetectorConfig(
            model_path="IDEA-Research/grounding-dino-base",
            prompts=[
                "a desk",
                "a keyboard",
                "a computer mouse",
                "a monitor",
                "headphones",
                "a can",
                "a chair"
            ],
            confidence_threshold=0.5
        )
    
    detector = OpenVocabularyDetector(detector_config)

    appearance_extractor = AppearanceExtractor()
    location_extractor = SemanticLocationExtractor()

    evidence_builder = EvidenceBuilder(appearance_extractor, location_extractor)

    perception_engine = PerceptionEngine(sensor, detector, evidence_builder)

    world_model = WorldModel()

    for i in range(2):
        perception_result = perception_engine.process()

        events = world_model.update(perception_result)

        print(f"FRAME {i}")
        print("OBJECTS:")
        print(list(world_model.objects))

        print("EVENTS:")
        print(events)

if __name__ == "__main__":
    main()