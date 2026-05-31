from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = Path(os.getenv("MODEL_DIR", ROOT_DIR / "models"))


@dataclass(frozen=True)
class ModelFile:
    name: str
    env_var: str
    filename: str
    required: bool = True

    @property
    def path(self) -> Path:
        value = os.getenv(self.env_var)
        return Path(value) if value else MODEL_DIR / self.filename


MODEL_FILES = (
    ModelFile("YOLO detector", "KGO_YOLO_CHECKPOINT", "Yolo26s_kgo.pt"),
    ModelFile("Crop classifier", "KGO_CROP_CLASSIFIER_CHECKPOINT", "best_efficientnet_v2_s_kgo.pth"),
    ModelFile("Full image classifier", "KGO_FULL_CLASSIFIER_CHECKPOINT", "best_efficientnet_for_full.pth"),
)

MODEL_REGISTRY_BASE_URL = os.getenv("MODEL_REGISTRY_BASE_URL", "").rstrip("/")
TARGET_DETECTION_CLASS = os.getenv("KGO_YOLO_CLASS_NAME", "kgo_platform")
