from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def iter_images(class_dir: Path):
    for path in class_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def validate_dataset(dataset: Path, classes: list[str], min_images_per_class: int) -> dict[str, int]:
    if not dataset.exists():
        raise AssertionError(f"Dataset directory does not exist: {dataset}")

    counts: dict[str, int] = {}
    for class_name in classes:
        class_dir = dataset / class_name
        if not class_dir.is_dir():
            raise AssertionError(f"Missing class directory: {class_dir}")

        images = list(iter_images(class_dir))
        if len(images) < min_images_per_class:
            raise AssertionError(
                f"Class '{class_name}' has {len(images)} images, expected at least {min_images_per_class}"
            )

        for image_path in images:
            with Image.open(image_path) as image:
                image.verify()
            if image_path.stat().st_size == 0:
                raise AssertionError(f"Empty image file: {image_path}")

        counts[class_name] = len(images)
    return counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate image dataset quality before training/inference.")
    parser.add_argument("--dataset", type=Path, default=Path("data/raw"))
    parser.add_argument("--classes", nargs="+", default=["kgo_empty", "kgo_full"])
    parser.add_argument("--min-images-per-class", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    counts = validate_dataset(args.dataset, args.classes, args.min_images_per_class)
    for class_name, count in counts.items():
        print(f"{class_name}: {count}")


if __name__ == "__main__":
    main()
