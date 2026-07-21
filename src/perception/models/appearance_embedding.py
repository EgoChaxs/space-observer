from dataclasses import dataclass
import numpy as np


@dataclass(slots=True, frozen=True)
class AppearanceEmbedding:
    """
    Represents the visual embedding of an observed object.

    The embedding is a high-dimensional feature vector describing the
    object's appearance and can be used for similarity comparison.

    Attributes:
        vector: Feature vector describing the object's appearance.
    """

    vector: np.ndarray