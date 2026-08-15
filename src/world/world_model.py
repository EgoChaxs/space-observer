import numpy as np
from uuid import UUID, uuid4

from configs.world.world_model_config import WorldModelConfig
from src.perception.models.perception_result import PerceptionResult
from src.perception.models.evidence import Evidence
from src.world.models.world_object import WorldObject
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

    def update(
        self, 
        perception_result: PerceptionResult
    ) -> tuple[list[Event], list[WorldObject]]:
        """
        Updates the world state using a new perception result.

        The update process consists of multiple stages:
            1. Resolve detected objects to existing WorldObjects or create new ones.
            2. Update object properties and relationships.
            3. Generate events caused by state transitions.
            4. Mark objects that are no longer observed as invisible.

        Args:
            perception_result: Result produced by the Perception subsystem
                containing detected objects and extracted evidence.

        Returns:
            A tuple containing a list of events describing changes detected during the update
            and a list of world objects that have been modified requiring persistance.
        """
        events: list[Event] = []
        modified_objects: list[WorldObject] = []

        detection_to_world_object: dict[UUID, WorldObject] = {}
        updated_objects: set[UUID] = set()
        created_objects: set[UUID] = set()

        # Pass 1 - Resolve object identities
        for evidence in perception_result.evidences:
            world_object = self._find_match(evidence)

            if world_object is None:
                world_object = WorldObject(
                    id=uuid4(),
                    label=evidence.detection.entity,
                    appearance_embedding=evidence.appearance_embedding.embedding,
                    semantic_location=None,
                    first_seen=perception_result.observation.timestamp,
                    last_seen=perception_result.observation.timestamp,
                    confidence=evidence.detection.confidence,
                    is_visible=True,
                )

                self._objects[world_object.id] = world_object
                created_objects.add(world_object.id)
                modified_objects.append(world_object)

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
                        timestamp=perception_result.observation.timestamp,
                        location=new_location
                    )
                )

            elif not was_visible:
                events.append(
                    self._event_generator.generate_object_reappeared(
                        object_id=world_object.id,
                        timestamp=perception_result.observation.timestamp,
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
                        timestamp=perception_result.observation.timestamp,
                        from_location=old_location,
                        to_location=new_location
                    )
                )

            # Apply updates
            world_object.appearance_embedding = evidence.appearance_embedding.embedding
            world_object.confidence = evidence.detection.confidence
            world_object.last_seen = perception_result.observation.timestamp
            world_object.is_visible = True
            if new_location is not None:
                world_object.semantic_location = new_location

            modified_objects.append(world_object)

        # Mark unseen objects as invisible
        unupdated_object_ids = self._objects.keys() - updated_objects

        for object_id in unupdated_object_ids:
            world_object = self._objects[object_id]

            if world_object.is_visible:
                events.append(
                    self._event_generator.generate_object_disappeared(
                        object_id=world_object.id,
                        timestamp=perception_result.observation.timestamp,
                        last_known_location=world_object.semantic_location
                    )
                )

            world_object.is_visible = False
            modified_objects.append(world_object)

        return events, modified_objects

    def _find_match(
        self, 
        evidence: Evidence
    ) -> WorldObject | None:
        """
        Finds the existing WorldObject corresponding to a perception evidence.

        Matching is performed by comparing object labels and appearance embedding
        similarity. If no existing object exceeds the similarity threshold, the
        evidence is considered to represent a new object.

        Args:
            evidence: Perception evidence containing detection information and
                appearance features.

        Returns:
            The matching WorldObject if one is found, otherwise None.
        """
        best_similarity = 0
        best_match: WorldObject | None = None

        for world_object in self._objects.values():

            if  world_object.label != evidence.detection.entity:
                continue

            similarity = self._compare(
                world_object,
                evidence
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = world_object

        if best_similarity < self._world_model_config.match_threshold:
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