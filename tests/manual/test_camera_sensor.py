import cv2
from pathlib import Path

from configs.perception.rf_detr_detector_config import RFDETRDetectorConfig
from configs.perception.camera_sensor_config import CameraSensorConfig
from configs.perception.appearance_extractor_config import AppearanceExtractorConfig
from configs.perception.detection_engine_config import DetectionEngineConfig
from configs.perception.observation_storage_config import ObservationStorageConfig
from configs.world.world_model_config import WorldModelConfig

from src.perception.detectors.rf_detr_detector import RFDETRDetector
from src.perception.sensors.camera_sensor import CameraSensor
from src.perception.extractors.appearance_extractor import AppearanceExtractor
from src.perception.extractors.semantic_location_extractor import SemanticLocationExtractor
from src.perception.builders.evidence_builder import EvidenceBuilder
from src.perception.engines.detection_engine import DetectionEngine
from src.perception.engines.perception_engine import PerceptionEngine
from src.world.world_model import WorldModel
from src.memory.memory import Memory

def main():
    memory = Memory()
    path_config = ObservationStorageConfig()

    sensor_config = CameraSensorConfig(
        sensor_id="bedroom_camera",
        name="Bedroom Camera",
        rtsp_address="rtsp://192.168.0.16:8554/live"
    )

    sensor = CameraSensor(sensor_config)
    memory.store_sensor(sensor_config)

    detector_config = RFDETRDetectorConfig(
        model_path="assets/models/rf_detr_small/rf-detr-small.pth",
        confidence_threshold=0.6
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

    state = memory.load_last_state() 

    world_model_config = WorldModelConfig()

    world_model = WorldModel(world_model_config, state)

    try:
        while True:
            perception_result = perception_engine.process()

            events, modified_objects = world_model.update(perception_result)

            for world_object in modified_objects:
                memory.store_object(world_object)

            if events:
                timestamp = perception_result.observation.timestamp.strftime(
                    "%Y-%m-%d_%H-%M-%S.%f"
                )

                path = (
                    Path(path_config.base_path)
                    / sensor_config.sensor_id
                    / f"{timestamp}.jpg"
                )

                path.parent.mkdir(parents=True, exist_ok=True)

                frame = cv2.cvtColor(
                    perception_result.observation.payload,
                    cv2.COLOR_RGB2BGR
                )

                if not cv2.imwrite(str(path), frame):
                    raise RuntimeError(
                        f"Failed to save observation to '{path}'"
                    )

                observation_id = memory.store_observation(
                    perception_result.observation,
                    str(path)
                )

                for event in events:
                    memory.store_event(event, observation_id)

            print(
                perception_result.observation.timestamp,
                perception_result.observation.payload.shape
            )

            if not perception_result.evidences:
                print("No objects detected.")
                continue

            for evidence in perception_result.evidences:
                print(evidence.detection.entity)

    except KeyboardInterrupt:
        print("Stopping Space Observer...")

    finally:
        memory.store_world_state(world_model.objects)
        sensor.close()

if __name__ == "__main__":
    main()