from configs.perception.open_vocabulary_detector_config import OpenVocabularyDetectorConfig
from configs.perception.yolo_detector_config import YOLODetectorConfig
from configs.perception.rf_detr_detector_config import RFDETRDetectorConfig
from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType
from configs.perception.appearance_extractor_config import AppearanceExtractorConfig
from configs.perception.detection_engine_config import DetectionEngineConfig
from configs.world.world_model_config import WorldModelConfig

from src.perception.detectors.open_vocabulary_detector import OpenVocabularyDetector
from src.perception.detectors.yolo_detector import YOLODetector
from src.perception.detectors.rf_detr_detector import RFDETRDetector
from src.perception.sensors.image_sensor import ImageSensor
from src.perception.extractors.appearance_extractor import AppearanceExtractor
from src.perception.extractors.semantic_location_extractor import SemanticLocationExtractor
from src.perception.builders.evidence_builder import EvidenceBuilder
from src.perception.engines.detection_engine import DetectionEngine
from src.perception.engines.perception_engine import PerceptionEngine

from src.world.world_model import WorldModel

from src.memory.memory import Memory

from debug.detection_visualizer import DetectionVisualizer

def main():

    sensor_config = ImageSensorConfig(
        sensor_id="test_dataset",
        source_type=ImageSourceType.FOLDER,
        path="assets/test_images/"
    )

    yolo_detector_config = YOLODetectorConfig(
        model_path="assets/models/yolo/yolo11m.pt",
        confidence_threshold=0.4
    )

    openvoc_detector_config = OpenVocabularyDetectorConfig(
            model_path="assets/models/grounding_dino",
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

    rfdetr_detector_config = RFDETRDetectorConfig(
        model_path="assets/models/rf_detr_small/rf-detr-small.pth",
        confidence_threshold=0.5
    )

    detection_engine_config = DetectionEngineConfig(
        enable_post_processing=False,
        min_area_ratio=0.001,
        max_area_ratio=0.5
    )

    appearance_extractor_config = AppearanceExtractorConfig(
        model_path="assets/models/dinov3"
    )

    world_model_config = WorldModelConfig()

    sensor = ImageSensor(sensor_config)
    yolo_detector = YOLODetector(yolo_detector_config)
    openvoc_detector = OpenVocabularyDetector(openvoc_detector_config)
    rfdetr_detector = RFDETRDetector(rfdetr_detector_config)
    
    appearance_extractor = AppearanceExtractor(appearance_extractor_config)
    location_extractor = SemanticLocationExtractor()

    evidence_builder = EvidenceBuilder(appearance_extractor, location_extractor)

    detection_engine = DetectionEngine(detection_engine_config, rfdetr_detector)
    perception_engine = PerceptionEngine(sensor, detection_engine, evidence_builder)

    memory = Memory()
    last_state = memory.load_last_state()
    print(last_state)

    world_model = WorldModel(world_model_config, last_state)

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

    memory.store_world_state(world_model.objects)

if __name__ == "__main__":
    main()