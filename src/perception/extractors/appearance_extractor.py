import numpy as np
import torch
from transformers import AutoImageProcessor, AutoModel

from src.perception.models.appearance_embedding import AppearanceEmbedding
from src.perception.models.detection import Detection, BoundingBox
from src.perception.models.observation import Observation


class AppearanceExtractor:
    """
    Extracts visual appearance features from detected objects.

    Uses a vision model to convert cropped object images into appearance
    embeddings that can later be compared for object similarity.
    """
    def __init__(self, model_name: str = "facebook/dinov3-vits16-pretrain-lvd1689m"):
        """
        Initializes the appearance extractor.

        Args:
            model_name: Name or path of the pretrained vision model used to generate appearance embeddings.
        """
        self._processor = AutoImageProcessor.from_pretrained(model_name)
        self._model = AutoModel.from_pretrained(model_name)

    def extract(self, observation: Observation, detection: Detection) -> AppearanceEmbedding:
        """
        Extracts an appearance embedding for a detected object.

        The detection bounding box is used to crop the object's pixels from the
        observation payload. The cropped image is then processed by the vision
        model to generate a feature representation.

        Args:
            observation: Observation containing the raw sensor payload.
            detection: Detection describing the object region to extract.

        Returns:
            AppearanceEmbedding containing the object's visual feature vector.
        """

        crop = self._crop(observation.payload, detection.bounding_box)

        embedding = self._encode(crop)

        return AppearanceEmbedding(
            embedding=embedding
        )
    
    def _crop(self, payload: np.ndarray, bbox: BoundingBox) -> np.ndarray:
        """
        Crops an object region from an image payload using bounding box coordinates.

        Args:
            payload: Image array containing RGB pixel data.
            bbox: Bounding box defining the object region.

        Returns:
            Cropped image containing only the detected object region.
        """
        return payload[
            int(bbox.y1):int(bbox.y2), 
            int(bbox.x1):int(bbox.x2)
        ]

    def _encode(self, cropped_image: np.ndarray) -> np.ndarray:
        """
        Generates an appearance embedding from a cropped image.

        The image is preprocessed using the model processor and passed through
        the vision model to obtain a feature representation.

        Args:
            cropped_image: Cropped RGB image containing the detected object.

        Returns:
            Numpy array containing the object's appearance embedding vector.
        """
        inputs = self._processor(
            images=cropped_image,
            return_tensors="pt"
        )

        with torch.no_grad():
            outputs = self._model(**inputs)

        embedding = outputs.last_hidden_state[:, 0]

        return embedding.squeeze(0).cpu().numpy()