from sqlalchemy import Column, Integer, Text, BLOB, REAL
from sqlalchemy.orm import relationship
from src.database.database import Base

class ObjectModel(Base):
    __tablename__ = "object"

    # Columns
    object_id = Column(Integer, primary_key=True)
    world_object_uuid = Column(Text, unique=True, nullable=False)
    label = Column(Text, nullable=False)
    appearance_embedding = Column(BLOB, nullable=False)
    semantic_location = Column(Text, nullable=True)
    first_seen = Column(Text, nullable=False)
    last_seen = Column(Text, nullable=False)
    confidence = Column(REAL, nullable=False)
    is_visible = Column(Integer, nullable=False)

    # Relationships
    events = relationship(
        "EventModel",
        back_populates="object"
    )