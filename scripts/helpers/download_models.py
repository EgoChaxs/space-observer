import sys
from pathlib import Path
from urllib.request import urlretrieve

from huggingface_hub import snapshot_download


RFDETR_URL = (
    "https://storage.googleapis.com/"
    "rfdetr/small_coco/checkpoint_best_regular.pth"
)

RFDETR_PATH = Path("assets/models/rf_detr_small/rf-detr-small.pth")
DINO_DIR = Path("assets/models/dinov2")


def download_rfdetr():
    RFDETR_PATH.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = RFDETR_PATH.with_suffix(".pth.tmp")

    try:
        urlretrieve(RFDETR_URL, temporary_path)
        temporary_path.replace(RFDETR_PATH)
    except Exception:
        if temporary_path.exists():
            temporary_path.unlink()
        raise


def download_dinov2():
    temporary_dir = DINO_DIR.with_name("dinov2.tmp")

    if temporary_dir.exists():
        import shutil
        shutil.rmtree(temporary_dir)

    try:
        snapshot_download(
            repo_id="facebook/dinov2-small",
            local_dir=temporary_dir,
        )

        if DINO_DIR.exists():
            import shutil
            shutil.rmtree(DINO_DIR)

        temporary_dir.replace(DINO_DIR)

    except Exception:
        if temporary_dir.exists():
            import shutil
            shutil.rmtree(temporary_dir)
        raise


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_models.py [rfdetr|dinov2]")
        sys.exit(1)

    model = sys.argv[1].lower()

    if model == "rfdetr":
        download_rfdetr()
    elif model == "dinov2":
        download_dinov2()
    else:
        print(f"Unknown model: {model}")
        sys.exit(1)