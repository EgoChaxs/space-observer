from dataclasses import dataclass
from uuid import UUID

from src.world.events.event import Event


@dataclass(slots=True, frozen=True)
class ObjectMovedEvent(Event):
    """
    Event generated when an object changes its semantic location.

    Inherits:
        object_id: Identifier of the object that moved.
        timestamp: Time when the movement occurred.

    Attributes:
        from_location: Previous location of the object before the move.
        to_location: New location of the object after the move.
    """

    from_location: UUID
    to_location: UUID

    @property
    def payload(self) -> dict:
        """Return the event-specific data for database storage."""
        return {
            "from_location": (
                str(self.from_location)
                if self.from_location is not None
                else None
            ),
            "to_location": (
                str(self.to_location)
                if self.to_location is not None
                else None
            ),
        }