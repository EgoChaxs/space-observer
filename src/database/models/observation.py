from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

class ObservationModel(Base):
    __tablename__ = "observation"

    # Columns
    observation_id = Column(Integer, primary_key=True)
    timestamp = Column(Text, nullable=False)
    path = Column(Text, nullable=False)

    # Foreign key
    sensor_id = Column(
        Integer,
        ForeignKey("sensor.sensor_id"),
        nullable=False
    )

    # Relationships
    events = relationship(
        "EventModel",
        back_populates="observation"
    )

    sensor = relationship(
        "SensorModel",
        back_populates="observations"
    )