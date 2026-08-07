import numpy as np

from configs.perception.yolo_detector_config import YOLODetectorConfig
from configs.perception.appearance_extractor_config import AppearanceExtractorConfig
from configs.perception.detection_engine_config import DetectionEngineConfig
from src.perception.detectors.yolo_detector import YOLODetector
from src.perception.sensors.image_sensor import ImageSensor
from src.perception.engines.detection_engine import DetectionEngine
from src.perception.extractors.appearance_extractor import AppearanceExtractor
from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType


def main():

    sensor_config = ImageSensorConfig(
        sensor_id="test_dataset",
        source_type=ImageSourceType.FILE,
        path="assets/test_images/img1.jpg"
    )

    sensor = ImageSensor(sensor_config)

    observation = sensor.capture()

    detector_config = YOLODetectorConfig(
        model_path="assets/models/yolo/yolo11n.pt",
        confidence_threshold=0.5
    )
    detector = YOLODetector(detector_config)

    appearance_extractor_config = AppearanceExtractorConfig(
        model_path="assets/models/dinov3"
    )

    detection_engine_config = DetectionEngineConfig()

    engine = DetectionEngine(detection_engine_config, detector)

    detections = engine.run(observation)

    appearance_extractor = AppearanceExtractor(appearance_extractor_config)

    appearance = appearance_extractor.extract(observation, detections[0])

    norm = np.linalg.norm(appearance.embedding)

    print(detections)
    print(appearance.embedding.shape)
    print(norm)


if __name__ == "__main__":
    main()