import math

from src.perception.models.semantic_location import SemanticLocation
from src.perception.models.detection import Detection
from src.perception.models.observation import Observation

LOCATION_CANDIDATES = {
    "desk",
    "table",
    "shelf",
    "bed",
    "chair",
    "floor",
    "cabinet",
    "box",
}

class SemanticLocationExtractor:
    """
    Estimates the semantic location of objects using geometric
    relationships between detections.

    The extractor identifies nearby environment objects such as desks,
    tables, or shelves and assigns them as the likely location of
    the detected object.
    """

    def extract(self, observation: Observation, detection: Detection, detections: list[Detection]) -> SemanticLocation | None:
        """
        Extract the semantic location of an object.

        Finds the most likely location candidate among all detections
        using geometric relationships between bounding boxes.

        Args:
            observation: Observation containing the original sensor payload.
                Currently unused but kept for consistency with extractors.
            detection: Detection whose location is being estimated.
            detections: All detections from the current observation.

        Returns:
            SemanticLocation referencing the detected object that most
            likely represents the object's location, or None if no suitable
            candidate is found.
        """
        best_candidate = self._find_best_candidate(detection, detections)

        if best_candidate is None:
            return None

        return SemanticLocation(
            best_candidate.id
        )

    def _find_best_candidate(self, detection: Detection, detections: list[Detection]) -> Detection | None:
        """
        Find the highest scoring location candidate for an object.

        Filters detections to only include possible location objects,
        calculates a geometric score for each candidate, and returns
        the candidate with the highest score.

        Args:
            detection: Detection whose location is being determined.
            detections: All detections from the current observation.

        Returns:
            The detection representing the most likely location object,
            or None if no valid candidates exist.
        """
        candidates = []

        for candidate in detections:
            if candidate.id == detection.id:
                continue

            if not self._is_location_candidate(candidate):
                continue

            score = self._calculate_location_score(detection, candidate)

            candidates.append((candidate, score))

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda item: item[1]
        )[0]

    def _calculate_location_score(self, detection: Detection, candidate: Detection) -> float:
        """
        Calculate how likely a candidate is to be the object's location.

        The score combines multiple geometric signals:
        - horizontal overlap
        - vertical distance
        - relative area
        - containment relationship

        Args:
            detection: Object being located.
            candidate: Potential location object.

        Returns:
            A normalized score where higher values indicate a more likely
            semantic location candidate.
        """
        overlap_score = self._horizontal_overlap(detection, candidate)
        closeness_score = self._vertical_gap(detection, candidate)
        size_score = self._area_ratio(detection, candidate)
        containment_bonus = 1.0 if self._is_inside_candidate(detection, candidate) else 0.0

        return (
            overlap_score * 0.35
            + closeness_score * 0.35
            + size_score * 0.20
            + containment_bonus * 0.10
        )

    def _vertical_gap(self, detection: Detection, candidate: Detection) -> float:
        """
        Calculate the vertical proximity between two detections.

        Measures the distance between the object's bounding box and the
        candidate location bounding box. Smaller distances produce higher
        scores.

        Args:
            detection: Object being located.
            candidate: Potential location object.

        Returns:
            A normalized proximity score between 0 and 1.
        """
        box = detection.bounding_box
        candidate_box = candidate.bounding_box

        distance = abs(candidate_box.y1 - box.y2)

        return 1 / (1 + distance)

    def _horizontal_overlap(self, detection: Detection, candidate: Detection) -> float:
        """
        Calculate horizontal overlap between two bounding boxes.

        A high overlap indicates that the object is visually aligned
        with the candidate location, such as a keyboard aligned with
        a desk.

        Args:
            detection: Object being located.
            candidate: Potential location object.

        Returns:
            A normalized overlap score between 0 and 1.
        """
        box = detection.bounding_box
        candidate_box = candidate.bounding_box

        width = box.x2 - box.x1

        if width <= 0:
            return 0.0

        overlap_width = max(0.0, min(box.x2, candidate_box.x2) - max(box.x1, candidate_box.x1))

        return overlap_width / width

    def _is_inside_candidate(self, detection: Detection, candidate: Detection) -> bool:
        """
        Check whether an object bounding box is contained inside another.

        This helps identify cases where an object appears inside a larger
        location object, such as an item inside a box.

        Args:
            detection: Object being located.
            candidate: Potential containing location object.

        Returns:
            True if the object's bounding box is completely inside the
            candidate bounding box, otherwise False.
        """
        box = detection.bounding_box
        candidate_box = candidate.bounding_box

        return (
            box.x1 >= candidate_box.x1
            and box.x2 <= candidate_box.x2
            and box.y1 >= candidate_box.y1
            and box.y2 <= candidate_box.y2
        )

    def _area_ratio(self, detection: Detection, candidate: Detection) -> float:
        """
        Calculate the relative size difference between two detections.

        Larger location objects are generally more likely to contain or
        support smaller objects. A logarithmic normalization prevents very
        large objects from dominating the score.

        Args:
            detection: Object being located.
            candidate: Potential location object.

        Returns:
            A normalized area ratio score between 0 and 1.
        """
        ratio = self._area(candidate) / self._area(detection)

        if ratio <= 0:
            return 0.0

        return min(math.log1p(ratio) / math.log1p(100), 1.0)

    def _area(self, detection: Detection) -> float:
        """
        Calculate the pixel area of a detection bounding box.

        Args:
            detection: Detection whose bounding box area is calculated.

        Returns:
            Area of the bounding box in pixels.
        """
        bbox = detection.bounding_box

        return (bbox.x2 - bbox.x1) * (bbox.y2 - bbox.y1)

    def _is_location_candidate(self, detection: Detection) -> bool:
        """
        Determine whether a detection can represent a location object.

        Compares the normalized detection label against known location
        categories such as desks, tables, shelves, or boxes.

        Args:
            detection: Detection to evaluate.

        Returns:
            True if the detection represents a possible location object,
            otherwise False.
        """
        return self._normalize_label(detection.entity) in LOCATION_CANDIDATES

    def _normalize_label(self, label: str) -> str:
        """
        Normalize detector labels for comparison.

        Removes detector-specific formatting differences such as articles
        ("a desk" -> "desk") and converts labels to lowercase.

        Args:
            label: Raw label produced by the detector.

        Returns:
            Normalized label string.
        """
        return label.lower().removeprefix("a ")