# Models

This directory contains the machine learning model weights used by Space Observer.

Model weights are not tracked by Git because they are binary files that can be large and can change independently from the source code.

## YOLO

The current object detection implementation uses a YOLO model through the Ultralytics framework.

Expected structure:
```
models/
└── yolo11n.pt
```

To use the YOLO detector, place the model weights in this directory and update the detector configuration with the correct path:

```python
YOLODetectorConfig(
    model_path="assets/models/yolo11n.pt",
    confidence_threshold=0.5
)
```