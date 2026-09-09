import numpy as np
from datetime import datetime
from uuid import UUID, uuid4

from configs.world.world_model_config import WorldModelConfig
from src.perception.models.perception_result import PerceptionResult
from src.perception.models.evidence import Evidence
from src.world.models.world_object import WorldObject
from src.world.models.track import Track, TrackState
from src.world.events.event import Event
from src.world.generators.event_generator import EventGenerator


class WorldModel:
    """
    Maintains the current representation of the observed environment.

    The World Model receives PerceptionResult objects and incrementally updates
    its internal collection of WorldObjects. It is responsible for resolving
    object identities across observations, updating object state, detecting
    state transitions, and generating events describing changes in the world.

    The World Model does not perform perception itself. It relies on the
    Perception subsystem for observations and detections, and produces events
    that can later be consumed by systems such as Memory.
    """
    def __init__(
        self,
        config: WorldModelConfig,
        world_model_state: dict[UUID, WorldObject] | None = None
    ):
        """
        Initializes an empty world state.

        Args:
            config: Configuration for World Model behavior.
            world_model_state: The last known state of the world otherwise empty dict by default.

        The World Model starts without any known objects. Objects are created
        and added as they are discovered through incoming perception results.
        """
        self._world_model_config = config
        self._objects: dict[UUID, WorldObject] = world_model_state if world_model_state is not None else {}
        self._event_generator = EventGenerator()
        self._tracks: dict[UUID, Track] = {}

    def update(
        self, 
        perception_result: PerceptionResult
    ) -> tuple[list[Event], list[WorldObject]]:
        """
        Updates the world state using a new perception result.

        The update process consists of multiple stages:
            1. Resolve detected objects using recent tracking information and
            normal WorldObject matching.
            2. Update object properties and relationships.
            3. Generate events caused by state transitions.
            4. Mark objects that are no longer observed as invisible and move
            their tracks to the LOST state.
            5. Remove tracking entries that have been lost for too long.

        Args:
            perception_result: Result produced by the Perception subsystem
                containing detected objects and extracted evidence.

        Returns:
            A tuple containing a list of events describing changes detected during
            the update and a list of world objects that have been modified
            requiring persistence.
        """
        events: list[Event] = []
        modified_objects: list[WorldObject] = []

        detection_to_world_object: dict[UUID, WorldObject] = {}
        updated_objects: set[UUID] = set()
        created_objects: set[UUID] = set()
        used_object_ids: set[UUID] = set()

        timestamp = perception_result.observation.timestamp

        # Pass 1 - Resolve object identities
        for evidence in perception_result.evidences:

            # First, we try to recover a recently lost track.
            world_object = self._find_track_match(
                evidence,
                used_object_ids,
                timestamp
            )

            # If no lost track can be recovered, use normal WorldObject matching.
            if world_object is None:
                world_object = self._find_match(
                    evidence,
                    used_object_ids
                )

            # No existing identity could be associated with this detection => create new object
            if world_object is None:
                world_object = WorldObject(
                    id=uuid4(),
                    label=evidence.detection.entity,
                    appearance_embedding=evidence.appearance_embedding.embedding,
                    semantic_location=None,
                    first_seen=timestamp,
                    last_seen=timestamp,
                    confidence=evidence.detection.confidence,
                    is_visible=True,
                )

                self._objects[world_object.id] = world_object

                created_objects.add(world_object.id)
                modified_objects.append(world_object)

                # Every newly created WorldObject immediately gets a track.
                self._tracks[world_object.id] = Track(
                    object_id=world_object.id,
                    state=TrackState.TRACKED,
                )

            # This object was successfully associated with a detection.
            else:
                # Helps avoid same world object targeting
                used_object_ids.add(world_object.id)

                track = self._tracks.get(world_object.id)

                if track is None:
                    # This can happen for WorldObjects loaded from persistent
                    # storage when they have not yet been observed in this session.
                    self._tracks[world_object.id] = Track(
                        object_id=world_object.id,
                        state=TrackState.TRACKED,
                    )

                else:
                    track.state = TrackState.TRACKED
                    track.lost_since = None

            updated_objects.add(world_object.id)

            detection_to_world_object[evidence.detection.id] = world_object

        # Pass 2 - Update object state and relationships
        for evidence in perception_result.evidences:
            world_object = detection_to_world_object[evidence.detection.id]

            was_visible = world_object.is_visible
            old_location = world_object.semantic_location

            location_world_object = None

            # Resolve new location
            if evidence.semantic_location is not None:
                location_world_object = detection_to_world_object.get(
                    evidence.semantic_location.location_detection_id
                )

            new_location = None

            if location_world_object is not None:
                new_location = location_world_object.id

            # Generate appeared / reappeared event
            if world_object.id in created_objects:
                events.append(
                    self._event_generator.generate_object_appeared(
                        object_id=world_object.id,
                        timestamp=timestamp,
                        location=new_location
                    )
                )

            elif not was_visible:
                events.append(
                    self._event_generator.generate_object_reappeared(
                        object_id=world_object.id,
                        timestamp=timestamp,
                        location=new_location
                    )
                )

            # Generate moved event
            if (
                old_location is not None
                and new_location is not None
                and old_location != new_location
            ):
                events.append(
                    self._event_generator.generate_object_moved(
                        object_id=world_object.id,
                        timestamp=timestamp,
                        from_location=old_location,
                        to_location=new_location
                    )
                )

            # Apply updates
            world_object.appearance_embedding = (
                evidence.appearance_embedding.embedding
            )
            world_object.confidence = evidence.detection.confidence
            world_object.last_seen = timestamp
            world_object.is_visible = True

            if new_location is not None:
                world_object.semantic_location = new_location

            modified_objects.append(world_object)

        # Pass 3 - Mark unseen objects as invisible and their tracks as LOST
        unupdated_object_ids = self._objects.keys() - updated_objects

        for object_id in unupdated_object_ids:
            world_object = self._objects[object_id]

            if world_object.is_visible:
                events.append(
                    self._event_generator.generate_object_disappeared(
                        object_id=world_object.id,
                        timestamp=timestamp,
                        last_known_location=world_object.semantic_location
                    )
                )

            world_object.is_visible = False
            modified_objects.append(world_object)

            track = self._tracks.get(object_id)

            if track is not None and track.state == TrackState.TRACKED:
                track.state = TrackState.LOST
                track.lost_since = timestamp

        # Pass 4 - Remove expired tracks
        expired_track_ids: list[UUID] = []

        for object_id, track in self._tracks.items():
            if track.state != TrackState.LOST:
                continue

            if track.lost_since is None:
                continue

            lost_duration = (
                timestamp - track.lost_since
            ).total_seconds()

            if lost_duration >= self._world_model_config.track_timeout_seconds:
                expired_track_ids.append(object_id)

        for object_id in expired_track_ids:
            del self._tracks[object_id]

        return events, modified_objects

    def _find_match(
        self, 
        evidence: Evidence,
        excluded_ids: set[UUID] 
    ) -> WorldObject | None:
        """
        Finds the existing WorldObject corresponding to a perception evidence.

        Matching is performed by comparing object labels and appearance embedding
        similarity. If no existing object exceeds the similarity threshold, the
        evidence is considered to represent a new object.

        Args:
            evidence: Perception evidence containing detection information and
                appearance features.
            excluded_ids: something.

        Returns:
            The matching WorldObject if one is found, otherwise None.
        """
        best_similarity = 0.0
        best_match: WorldObject | None = None

        for world_object in self._objects.values():

            if world_object.id in excluded_ids:
                continue

            if  world_object.label != evidence.detection.entity:
                continue

            similarity = self._compare(
                world_object,
                evidence
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = world_object

        matched = best_similarity >= self._world_model_config.match_threshold

        print(
            f"{evidence.detection.entity}: "
            f"best_similarity={best_similarity:.4f}, "
            f"threshold={self._world_model_config.match_threshold:.2f}, "
            f"matched={matched}, "
            f"match_id={best_match.id if best_match else None}"
        )

        if not matched:
            return None

        return best_match

    def _find_track_match(
        self,
        evidence: Evidence,
        used_object_ids: set[UUID],
        timestamp: datetime,
    ) -> WorldObject | None:
        """
        Finds a recently lost WorldObject that can be associated with an
        incoming detection.

        Only LOST tracks within the configured tracking timeout are considered.
        A WorldObject that has already been assigned to another detection in the
        same observation is ignored.

        Args:
            evidence: Evidence associated with the incoming detection.
            used_object_ids: WorldObject IDs already assigned during this update.
            timestamp: Timestamp of the current observation.

        Returns:
            The best matching WorldObject, or None if no suitable track exists.
        """
        best_similarity = 0.0
        best_match: WorldObject | None = None

        for object_id, track in self._tracks.items():
            if track.state != TrackState.LOST:
                continue

            if object_id in used_object_ids:
                continue

            if track.lost_since is None:
                continue

            lost_duration = (
                timestamp - track.lost_since
            ).total_seconds()

            if lost_duration >= self._world_model_config.track_timeout_seconds:
                continue

            world_object = self._objects.get(object_id)

            if world_object is None:
                continue

            if world_object.label != evidence.detection.entity:
                continue

            similarity = self._compare(
                world_object,
                evidence
            )

            print(
                f"[TRACK] {evidence.detection.entity}: "
                f"candidate={object_id}, "
                f"similarity={similarity:.4f}, "
                f"threshold={self._world_model_config.match_threshold:.2f}"
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = world_object

        if best_match is None:
            print(
                f"[TRACK] {evidence.detection.entity}: "
                f"no candidate found"
            )
            return None

        matched = best_similarity >= self._world_model_config.match_threshold

        print(
            f"[TRACK] {evidence.detection.entity}: "
            f"best_similarity={best_similarity:.4f}, "
            f"matched={matched}, "
            f"match_id={best_match.id}"
        )

        if not matched:
            return None

        return best_match

    def _compare(
        self, 
        world_object: WorldObject, 
        evidence: Evidence
    ) -> float:
        """
        Computes appearance similarity between a known object and new evidence.

        The comparison uses cosine similarity through the dot product of normalized
        appearance embeddings.

        Args:
            world_object: Existing object stored in the World Model.
            evidence: New perception evidence to compare against.

        Returns:
            Similarity score between the two appearance embeddings.
        """
        return np.dot(
            world_object.appearance_embedding, 
            evidence.appearance_embedding.embedding
        )

    @property
    def objects(self) -> dict[UUID, WorldObject]:
        """
        Provides access to the currently known world objects.

        Returns:
            A collection containing all WorldObjects tracked by the World Model.
        """
        return self._objects