from src.perception.image_sensor import ImageSensor
from src.perception.image_config import ImageSensorConfig, ImageSourceType


config = ImageSensorConfig(
    source_type=ImageSourceType.FOLDER,
    path=r"C:\Users\inibu\Pictures\Anime pictures"
)

sensor = ImageSensor(config)


for _ in range(50):
    observation = sensor.capture()

    print(observation.id)
    print(observation.timestamp)
    print(observation.payload.shape)
    print("----------------")