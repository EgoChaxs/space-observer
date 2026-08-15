from dataclasses import dataclass
from uuid import UUID

from src.world.events.event import Event


@dataclass(slots=True, frozen=True)
class ObjectReappearedEvent(Event):
    """
    Event generated when an object becomes visible again after previously
    being marked as disappeared by the World Model.

    Inherits:
        object_id: Identifier of the object that reappeared.
        timestamp: Time when the object was detected again.

    Attributes:
        location: Location where the object was observed, if available.
    """

    location: UUID | None

    @property
    def payload(self) -> dict:
        """Return the event-specific data for database storage."""
        return {
            "location": (
                str(self.location)
                if self.location is not None
                else None
            )
        }