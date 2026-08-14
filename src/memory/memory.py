from datetime import datetime
from uuid import UUID

import numpy as np

from src.database.database import SessionLocal
from src.database.models.world_state_snapshot import WorldStateModel
from src.world.models.world_object import WorldObject

class Memory:
    def store_sensor(self, sensor):
        ...

    def store_observation(self, observation):
        ...

    def store_event(self, event):
        ...

    def store_object(self, world_object):
        ...

    def store_world_state(self, world_objects: dict[UUID, WorldObject]):
        data = {
            str(object_id): {
                "id": str(world_object.id),
                "label": world_object.label,
                "appearance_embedding": (
                    world_object.appearance_embedding.tolist()
                ),
                "semantic_location": (
                    str(world_object.semantic_location)
                    if world_object.semantic_location is not None
                    else None
                ),
                "first_seen": world_object.first_seen.isoformat(),
                "last_seen": world_object.last_seen.isoformat(),
                "confidence": world_object.confidence,
                "is_visible": world_object.is_visible,
            }
            for object_id, world_object in world_objects.items()
        }

        state = WorldStateModel(
            timestamp=datetime.now().isoformat(),
            world_data=data
        )

        with SessionLocal() as session:
            session.add(state)
            session.commit()

    def retrieve_object(self, object_id):
        ...

    def load_last_state(self) -> dict[UUID, WorldObject] | None:
        with SessionLocal() as session:
            state = (
                session.query(WorldStateModel)
                .order_by(WorldStateModel.state_id.desc())
                .first()
            )

        if state is None:
            return None

        world_objects = {}

        for object_id, data in state.world_data.items():
            world_object = WorldObject(
                id=UUID(data["id"]),
                label=data["label"],
                appearance_embedding=np.array(
                    data["appearance_embedding"],
                    dtype=np.float32
                ),
                semantic_location=(
                    UUID(data["semantic_location"])
                    if data["semantic_location"] is not None
                    else None
                ),
                first_seen=datetime.fromisoformat(data["first_seen"]),
                last_seen=datetime.fromisoformat(data["last_seen"]),
                confidence=data["confidence"],
                is_visible=bool(data["is_visible"]),
            )

            world_objects[UUID(object_id)] = world_object

        return world_objects