from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    "sqlite:///data/space_observer.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

from src.database.models import (
    SensorModel,
    ObservationModel,
    EventModel,
    ObjectModel,
    WorldStateModel,
)