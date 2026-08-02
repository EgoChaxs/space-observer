from dataclasses import dataclass
from uuid import UUID

from src.world.events.event import Event


@dataclass(slots=True, frozen=True)
class ObjectDisappearedEvent(Event):
    """
    Event generated when an object is no longer detected by the World Model.

    Inherits:
        object_id: Identifier of the object that moved.
        timestamp: Time when the movement occurred.
        
    Attributes:
        last_known_location: Last known location of the object before it
            disappeared, if available.
    """

    last_known_location: UUID | None