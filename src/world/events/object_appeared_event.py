from dataclasses import dataclass
from uuid import UUID

from src.world.events.event import Event


@dataclass(slots=True, frozen=True)
class ObjectAppearedEvent(Event):
    """
    Event generated when an object is first detected by the World Model.

    Inherits:
        object_id: Identifier of the object that moved.
        timestamp: Time when the movement occurred.
        
    Attributes:
        location: Location where the object was observed, if available.
    """

    location: UUID | None