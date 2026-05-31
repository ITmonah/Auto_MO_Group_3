from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from scripts.validate_data import validate_dataset


def create_image(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (16, 16), color=(32, 96, 64)).save(path)


def test_validate_dataset_accepts_expected_class_layout(tmp_path: Path) -> None:
    create_image(tmp_path / "kgo_empty" / "sample.png")
    create_image(tmp_path / "kgo_full" / "sample.png")

    counts = validate_dataset(tmp_path, ["kgo_empty", "kgo_full"], min_images_per_class=1)

    assert counts == {"kgo_empty": 1, "kgo_full": 1}


def test_validate_dataset_rejects_missing_class(tmp_path: Path) -> None:
    create_image(tmp_path / "kgo_empty" / "sample.png")

    with pytest.raises(AssertionError, match="Missing class directory"):
        validate_dataset(tmp_path, ["kgo_empty", "kgo_full"], min_images_per_class=1)
