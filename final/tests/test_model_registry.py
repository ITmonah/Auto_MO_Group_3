from __future__ import annotations

from app.config import MODEL_FILES
from app.model_registry import model_status


def test_model_registry_declares_external_model_files() -> None:
    filenames = {model.filename for model in MODEL_FILES}

    assert "Yolo26s_kgo.pt" in filenames
    assert "best_efficientnet_v2_s_kgo.pth" in filenames
    assert "best_efficientnet_for_full.pth" in filenames


def test_model_status_is_json_serializable_shape() -> None:
    status = model_status()

    assert status
    for item in status:
        assert {"name", "env_var", "filename", "path", "available"} <= set(item)
