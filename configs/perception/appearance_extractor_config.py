from dataclasses import dataclass


@dataclass(slots=True)
class AppearanceExtractorConfig:
    """
    Configuration for the appearance extractor.

    Attributes:
        model_path: Path to the local directory containing the pretrained
            vision model used to generate appearance embeddings.
    """

    model_path: str