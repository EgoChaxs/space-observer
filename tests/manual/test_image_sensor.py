from src.perception.sensor.image_sensor import ImageSensor
from configs.perception.image_sensor_config import ImageSensorConfig, ImageSourceType


config = ImageSensorConfig(
    sensor_id="test_dataset",
    source_type=ImageSourceType.FOLDER,
    path="assets/test_images/cat.jpg"
)

sensor = ImageSensor(config)


for _ in range(10):
    observation = sensor.capture()

    print(observation.id)
    print(observation.sensor_id)
    print(observation.timestamp)
    print(observation.payload.shape)
    print("----------------")