# Models

This directory contains the machine learning models used by Space Observer.

Model files are not tracked by Git because they can be large binary files and are managed independently from the source code.

All models must be installed locally before running Space Observer. The application does not automatically download missing models at runtime.

## YOLO

- Tested models: YOLO11n, YOLO11m
- Place `.pt` model files in `assets/models/yolo/`
- Other YOLO models may work, but are not guaranteed to be compatible.

Example:

```text
assets/models/yolo/
├── yolo11n.pt
└── yolo11m.pt
```

## RF-DETR

- Tested model: RF-DETR Small
- The weights must be compatible with RFDETRSmall.
- Place the weights in assets/models/rf_detr_small/

Example: 

```text
assets/models/rf_detr_small/
└── rf-detr-small.pth
```

## DINO

- Tested models: DINOv3 ViT-S/16
- The model must be compatible with the Hugging Face Transformers API.
- Place the complete local model directory in assets/models/dinov3/

## Grounding DINO

- Tested model: Grounding DINO Base
- The model must be compatible with the Hugging Face Transformers API.
- Place the complete local model directory in assets/models/grounding_dino/

## Warning

Do not put arbitrary model files into these directories and assume they will work.

Space Observer expects the model architecture and format required by the corresponding detector or extractor. Using an incompatible model may result in initialization errors or incorrect behavior.