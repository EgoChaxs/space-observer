from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class TrackState(Enum):
    """
    Lifecycle state of a tracked world object.

    A track represents short-term perception state, not persistent world
    knowledge. The associated WorldObject remains in the WorldModel even
    when its track is lost or removed.
    """

    TRACKED = "tracked"
    LOST = "lost"


@dataclass(slots=True)
class Track:
    """
    Represents the short-term tracking state of a WorldObject.

    A Track is used by the WorldModel to keep recently observed objects
    eligible for re-association after they temporarily disappear from
    perception.

    Tracks are intentionally separate from WorldObjects:

        WorldObject
            Long-term representation of an entity in the world.

        Track
            Short-term perception state used while associating observations
            with that entity.

    A track may be removed after an object has been lost for long enough.
    Removing a Track does not remove the associated WorldObject from the
    WorldModel.

    Attributes:
        object_id:
            ID of the WorldObject represented by this track.

        state:
            Current lifecycle state of the track.

        lost_since:
            Timestamp at which the object became lost. This is None while
            the object is currently tracked.

    Lifecycle:

        TRACKED
            The object is currently being observed.

        LOST
            The object has not been observed recently, but its identity is
            still kept temporarily for possible re-association.

        Track removed
            The lost timeout has expired. The WorldObject remains in the
            WorldModel, but the object is no longer considered a recent
            tracking candidate.
    """

    object_id: UUID
    state: TrackState
    lost_since: datetime | None = None