from configs.perception.rf_detr_detector_config import RFDETRDetectorConfig
from configs.perception.camera_sensor_config import CameraSensorConfig
from configs.perception.appearance_extractor_config import AppearanceExtractorConfig
from configs.perception.detection_engine_config import DetectionEngineConfig

from src.perception.detectors.rf_detr_detector import RFDETRDetector
from src.perception.sensors.camera_sensor import CameraSensor
from src.perception.extractors.appearance_extractor import AppearanceExtractor
from src.perception.extractors.semantic_location_extractor import SemanticLocationExtractor
from src.perception.builders.evidence_builder import EvidenceBuilder
from src.perception.engines.detection_engine import DetectionEngine
from src.perception.engines.perception_engine import PerceptionEngine


def main():

    sensor_config = CameraSensorConfig(
        sensor_id="Bedroom Camera",
        name="Bedroom Camera",
        rtsp_address="rtsp://192.168.0.16:8554/live"
    )

    sensor = CameraSensor(sensor_config)

    detector_config = RFDETRDetectorConfig(
        model_path="assets/models/rf_detr_small/rf-detr-small.pth"
    )
    
    detector = RFDETRDetector(detector_config)

    appearance_extractor_config = AppearanceExtractorConfig(
        model_path="assets/models/dinov2"
    )

    detection_engine_config = DetectionEngineConfig()

    appearance_extractor = AppearanceExtractor(appearance_extractor_config)
    location_extractor = SemanticLocationExtractor()

    evidence_builder = EvidenceBuilder(appearance_extractor, location_extractor)
    detection_engine = DetectionEngine(detection_engine_config, detector)

    perception_engine = PerceptionEngine(sensor, detection_engine, evidence_builder)

    

    while True:
        perception_result = perception_engine.process()

        print(
            perception_result.observation.timestamp,
            perception_result.observation.payload.shape
        )

        if not perception_result.evidences:
            print("No objects detected.")
            continue

        for evidence in perception_result.evidences:
            print(evidence.detection.entity)

if __name__ == "__main__":
    main()