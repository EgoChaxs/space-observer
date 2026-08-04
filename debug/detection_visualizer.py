import cv2

from src.perception.models.observation import Observation
from src.perception.models.detection import Detection


class DetectionVisualizer:
    """
    Utility for visualizing object detections on captured observations.

    The visualizer overlays detection bounding boxes and confidence scores
    onto an observation image, then saves the annotated result for debugging
    and inspection.
    """

    def visualize(
        self,
        observation: Observation,
        detections: list[Detection],
        output_path: str = "detection_debug.png"
    ) -> None:
        """
        Draw detections on an observation and save the annotated image.

        Args:
            observation: Observation containing the captured image.
            detections: Detections to visualize on the image.
            output_path: Where do you want them images to be stored? :D 
        """

        image = observation.payload.copy()

        for detection in detections:
            bbox = detection.bounding_box

            cv2.rectangle(
                image,
                (int(bbox.x1), int(bbox.y1)),
                (int(bbox.x2), int(bbox.y2)),
                (0, 255, 0),
                2
            )

            label = f"{detection.entity} {detection.confidence:.2f}"

            cv2.putText(
                image,
                label,
                (int(bbox.x1), int(bbox.y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        display_width = 1000
        scale = display_width / image.shape[1]
        display_height = int(image.shape[0] * scale)

        image = cv2.resize(
            image,
            (display_width, display_height)
        )

        cv2.imwrite(
            output_path,
            image
        )