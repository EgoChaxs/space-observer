from sqlalchemy import Column, Integer, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

class EventModel(Base):
    __tablename__ = "event"

    # Columns
    event_id = Column(Integer, primary_key=True)
    type = Column(Text, nullable=False)
    timestamp = Column(Text, nullable=False)
    data = Column(JSON, nullable=False)

    # Foreign Keys
    observation_id = Column(
        Integer,
        ForeignKey("observation.observation_id"),
        nullable=False
    )

    object_id = Column(
        Integer,
        ForeignKey("object.object_id"),
        nullable=False
    )

    # Relationships
    object = relationship(
        "ObjectModel",
        back_populates="events"
    )

    observation = relationship(
        "ObservationModel",
        back_populates="events"
    )