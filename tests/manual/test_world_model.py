from configs.perception.open_vocabulary_detector_config import OpenVocabularyDetectorConfig
from configs.perception.yolo_detector_config import YOLODetectorConfig
from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType
from configs.perception.detection_engine_config import DetectionEngineConfig
from src.perception.detectors.open_vocabulary_detector import OpenVocabularyDetector
from src.perception.detectors.yolo_detector import YOLODetector
from src.perception.sensors.image_sensor import ImageSensor
from src.perception.extractors.appearance_extractor import AppearanceExtractor
from src.perception.extractors.semantic_location_extractor import SemanticLocationExtractor
from src.perception.builders.evidence_builder import EvidenceBuilder
from src.perception.engines.detection_engine import DetectionEngine
from src.perception.engines.perception_engine import PerceptionEngine
from src.world.world_model import WorldModel

from debug.detection_visualizer import DetectionVisualizer

def main():

    sensor_config = ImageSensorConfig(
        sensor_id="test_dataset",
        source_type=ImageSourceType.FOLDER,
        path="assets/test_images/"
    )

    yolo_detector_config = YOLODetectorConfig(
        model_path="assets/models/yolo11m.pt",
        confidence_threshold=0.4
    )

    openvoc_detector_config = OpenVocabularyDetectorConfig(
            model_path="IDEA-Research/grounding-dino-base",
            prompts=[
                "a desk",
                "a keyboard",
                "a computer mouse",
                "a monitor",
                "headphones",
                "a can",
                "a chair",
                "a table"
            ],
            confidence_threshold=0.5
        )

    detection_engine_config = DetectionEngineConfig(
        enable_post_processing=False,
        min_area_ratio=0.001,
        max_area_ratio=0.5
    )

    sensor = ImageSensor(sensor_config)
    yolo_detector = YOLODetector(yolo_detector_config)
    openvoc_detector = OpenVocabularyDetector(openvoc_detector_config)
    
    appearance_extractor = AppearanceExtractor()
    location_extractor = SemanticLocationExtractor()

    evidence_builder = EvidenceBuilder(appearance_extractor, location_extractor)

    detection_engine = DetectionEngine(detection_engine_config, openvoc_detector)
    perception_engine = PerceptionEngine(sensor, detection_engine, evidence_builder)

    world_model = WorldModel()

    visualizer = DetectionVisualizer()

    for i in range(2):
        perception_result = perception_engine.process()

        visualizer.visualize(
            perception_result.observation,
            [evidence.detection for evidence in perception_result.evidences]
        )

        for evidence in perception_result.evidences:
            print(
                evidence.detection.entity,
                evidence.detection.confidence,
                evidence.detection.bounding_box
            )

        events = world_model.update(perception_result)

        for evidence in perception_result.evidences:
            print(f"DETECTED: {evidence.detection.entity} \n")

        print(f"FRAME {i}")
        print("OBJECTS:")
        print(list(world_model.objects))

        print("EVENTS:")
        print(events)

if __name__ == "__main__":
    main()