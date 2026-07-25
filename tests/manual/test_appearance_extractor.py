from configs.perception.yolo_detector_config import YOLODetectorConfig
from src.perception.detectors.yolo_detector import YOLODetector
from src.perception.sensors.image_sensor import ImageSensor
from src.perception.engines.detection_engine import DetectionEngine
from src.perception.extractors.appearance_extractor import AppearanceExtractor
from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType


def main():

    sensor_config = ImageSensorConfig(
        sensor_id="test_dataset",
        source_type=ImageSourceType.FILE,
        path="assets/test_images/desk_before.jpg"
    )

    sensor = ImageSensor(sensor_config)

    observation = sensor.capture()

    detector_config = YOLODetectorConfig(
        model_path="assets/models/yolo11n.pt",
        confidence_threshold=0.5
    )
    detector = YOLODetector(detector_config)

    engine = DetectionEngine(detector)

    detections = engine.run(observation)

    appearance_extractor = AppearanceExtractor()

    appearance = appearance_extractor.extract(observation, detections[0])

    print(detections)
    print(appearance.embedding.shape)


if __name__ == "__main__":
    main()