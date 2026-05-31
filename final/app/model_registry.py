from __future__ import annotations

import os
import urllib.request
from pathlib import Path

from app.config import MODEL_FILES, MODEL_REGISTRY_BASE_URL, ModelFile


class ModelRegistryError(RuntimeError):
    pass


def model_status() -> list[dict[str, object]]:
    return [
        {
            "name": model.name,
            "env_var": model.env_var,
            "filename": model.filename,
            "path": str(model.path),
            "available": model.path.exists(),
        }
        for model in MODEL_FILES
    ]


def missing_models() -> list[ModelFile]:
    return [model for model in MODEL_FILES if model.required and not model.path.exists()]


def _download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = destination.with_suffix(destination.suffix + ".tmp")
    try:
        urllib.request.urlretrieve(url, tmp_path)
        os.replace(tmp_path, destination)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def ensure_models(download: bool = True) -> None:
    unresolved = missing_models()
    if not unresolved:
        return

    if download:
        if not MODEL_REGISTRY_BASE_URL:
            names = ", ".join(model.filename for model in unresolved)
            raise ModelRegistryError(
                "Missing model files and MODEL_REGISTRY_BASE_URL is not set: " + names
            )

        for model in unresolved:
            _download_file(f"{MODEL_REGISTRY_BASE_URL}/{model.filename}", model.path)

    unresolved = missing_models()
    if unresolved:
        details = "; ".join(f"{model.name}: {model.path}" for model in unresolved)
        raise ModelRegistryError(f"Missing model files: {details}")
