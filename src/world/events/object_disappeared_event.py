from dataclasses import dataclass
from uuid import UUID

from src.world.events.event import Event


@dataclass(slots=True, frozen=True)
class ObjectDisappearedEvent(Event):
    """
    Event generated when an object is no longer detected by the World Model.

    Inherits:
        object_id: Identifier of the object that disappeared.
        timestamp: Time when the object disappeared.
        
    Attributes:
        last_known_location: Last known location of the object before it
            disappeared, if available.
    """

    last_known_location: UUID | None

    @property
    def payload(self) -> dict:
        """Return the event-specific data for database storage."""
        return {
            "last_known_location": (
                str(self.last_known_location)
                if self.last_known_location is not None
                else None
            )
        }