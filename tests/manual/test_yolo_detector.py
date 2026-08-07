from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType
from configs.perception.yolo_detector_config import YOLODetectorConfig
from configs.perception.detection_engine_config import DetectionEngineConfig

from src.perception.detectors.yolo_detector import YOLODetector
from src.perception.sensors.image_sensor import ImageSensor
from src.perception.engines.detection_engine import DetectionEngine



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

    detection_engine_config = DetectionEngineConfig()

    engine = DetectionEngine(detection_engine_config, detector)

    detections = engine.run(observation)

    print(detections)


if __name__ == "__main__":
    main()