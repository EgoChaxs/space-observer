from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from src.database.database import Base

class SensorModel(Base):
    __tablename__ = "sensor"

    # Columns
    sensor_id = Column(Integer, primary_key=True)
    sensor_uuid = Column(Text, unique=True, nullable=False)
    name = Column(Text, nullable=False)

    # Relationships
    observations = relationship(
        "ObservationModel",
        back_populates="sensor"
    )