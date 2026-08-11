import numpy as np

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

    dinov2_config = AppearanceExtractorConfig(
        model_path="assets/models/dinov2-small"
    )

    dinov3_config = AppearanceExtractorConfig(
        model_path="assets/models/dinov3"
    )

    world_model_config = WorldModelConfig()

    sensor = ImageSensor(sensor_config)

    yolo_detector = YOLODetector(yolo_detector_config)
    openvoc_detector = OpenVocabularyDetector(openvoc_detector_config)
    rfdetr_detector = RFDETRDetector(rfdetr_detector_config)

    dinov2 = AppearanceExtractor(dinov2_config)
    dinov3 = AppearanceExtractor(dinov3_config)

    location_extractor = SemanticLocationExtractor()

    # We do not use the appearance extractor here because we are
    # comparing DINOv2 and DINOv3 manually.
    evidence_builder = EvidenceBuilder(dinov2, location_extractor)

    detection_engine = DetectionEngine(
        detection_engine_config,
        rfdetr_detector
    )

    perception_engine = PerceptionEngine(
        sensor,
        detection_engine,
        evidence_builder
    )

    world_model = WorldModel(world_model_config)

    visualizer = DetectionVisualizer()

    dinov2_keyboard_embeddings = []
    dinov3_keyboard_embeddings = []

    first_keyboard_embedding_v2 = None
    first_keyboard_embedding_v3 = None

    for i in range(2):

        perception_result = perception_engine.process()

        detections = [
            evidence.detection
            for evidence in perception_result.evidences
        ]

        visualizer.visualize(
            perception_result.observation,
            detections
        )

        for detection in detections:
            print(
                detection.entity,
                detection.confidence,
                detection.bounding_box
            )

        keyboard = next(
            (
                detection
                for detection in detections
                if detection.entity == "keyboard"
            ),
            None
        )

        if keyboard is None:
            print(f"Keyboard not detected in frame {i}.")
            continue

        v2_embedding = dinov2.extract(
            perception_result.observation,
            keyboard
        ).embedding

        v3_embedding = dinov3.extract(
            perception_result.observation,
            keyboard
        ).embedding

        dinov2_keyboard_embeddings.append(v2_embedding)
        dinov3_keyboard_embeddings.append(v3_embedding)

        if i == 0:
            first_keyboard_embedding_v2 = v2_embedding
            first_keyboard_embedding_v3 = v3_embedding

        # Compare keyboard against other detected objects
        for detection in detections:
            if detection.entity == "keyboard":
                continue

            v2_other = dinov2.extract(
                perception_result.observation,
                detection
            ).embedding

            v3_other = dinov3.extract(
                perception_result.observation,
                detection
            ).embedding

            v2_similarity = np.dot(v2_embedding, v2_other)
            v3_similarity = np.dot(v3_embedding, v3_other)

            print(
                f"{detection.entity}: "
                f"DINOv2={v2_similarity:.4f}, "
                f"DINOv3={v3_similarity:.4f}"
            )

        events = world_model.update(perception_result)

        print(f"\nFRAME {i}")
        print("OBJECTS:")
        print(list(world_model.objects))

        print("EVENTS:")
        print(events)
        print()

    # Compare the keyboard between frames.
    if len(dinov2_keyboard_embeddings) == 2:
        v2_same_object = np.dot(
            dinov2_keyboard_embeddings[0],
            dinov2_keyboard_embeddings[1]
        )

        v3_same_object = np.dot(
            dinov3_keyboard_embeddings[0],
            dinov3_keyboard_embeddings[1]
        )

        print("=" * 50)
        print("CROSS-FRAME KEYBOARD SIMILARITY")
        print("=" * 50)

        print(f"DINOv2: {v2_same_object:.4f}")
        print(f"DINOv3: {v3_same_object:.4f}")


if __name__ == "__main__":
    main()