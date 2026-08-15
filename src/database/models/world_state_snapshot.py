from sqlalchemy import Column, Integer, Text, JSON
from src.database.database import Base

class WorldStateModel(Base):
    """
    Database model representing a snapshot of the World Model state.

    Stores the serialized state at a specific point in time.
    """
    
    __tablename__ = "world_state_snapshot"

    # Columns
    state_id = Column(Integer, primary_key=True)
    timestamp = Column(Text, nullable=False)
    world_data = Column(JSON, nullable=False)