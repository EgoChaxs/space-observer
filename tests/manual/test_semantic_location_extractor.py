from configs.perception.open_vocabulary_detector_config import OpenVocabularyDetectorConfig
from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType
from configs.perception.detection_engine_config import DetectionEngineConfig

from src.perception.detectors.open_vocabulary_detector import OpenVocabularyDetector
from src.perception.sensors.image_sensor import ImageSensor
from src.perception.engines.detection_engine import DetectionEngine
from src.perception.extractors.semantic_location_extractor import SemanticLocationExtractor



def main():

    sensor_config = ImageSensorConfig(
        sensor_id="test_dataset",
        source_type=ImageSourceType.FILE,
        path="assets/test_images/img1.jpg"
    )

    sensor = ImageSensor(sensor_config)

    observation = sensor.capture()

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
        confidence_threshold=0.25
    )
    detector = OpenVocabularyDetector(detector_config)

    detection_engine_config = DetectionEngineConfig()

    engine = DetectionEngine(detection_engine_config, detector)

    detections = engine.run(observation)

    location_extractor = SemanticLocationExtractor()

    location = location_extractor.extract(observation, detections[1], detections)

    print("DETECTIONS:")
    for detection in detections:
        print(detection.entity, detection.id)

    print("LOCATION:")
    print(location)



if __name__ == "__main__":
    main()