from __future__ import annotations

import base64
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from app.config import MODEL_FILES, TARGET_DETECTION_CLASS
from app.model_registry import ensure_models, model_status


CLASS_NAMES_FALLBACK = ["kgo_empty", "kgo_full"]


def image_to_data_url(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def _draw_overlay(image: Image.Image, label: str) -> Image.Image:
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    font = ImageFont.load_default()
    text = label or "kgo_platform not found"
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    padding = 8
    draw.rectangle((12, 12, 12 + width + padding * 2, 12 + height + padding * 2), fill="black")
    draw.text((12 + padding, 12 + padding), text, fill="white", font=font)
    return annotated


def _load_efficientnet(checkpoint_path: Path, device):
    import torch
    from torchvision.models import efficientnet_v2_s

    checkpoint = torch.load(str(checkpoint_path), map_location=device)
    if not isinstance(checkpoint, dict) or "state_dict" not in checkpoint:
        raise ValueError(f"Checkpoint has unsupported format: {checkpoint_path}")

    class_names = checkpoint.get("class_names", CLASS_NAMES_FALLBACK)
    model = efficientnet_v2_s(weights=None, num_classes=len(class_names))
    model.load_state_dict(checkpoint["state_dict"])
    model.to(device)
    model.eval()
    return model, list(class_names)


@lru_cache(maxsize=1)
def load_models():
    ensure_models(download=True)

    import torch
    import torchvision.transforms as transforms
    from ultralytics import YOLO

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    paths = {model.env_var: model.path for model in MODEL_FILES}
    detector = YOLO(str(paths["KGO_YOLO_CHECKPOINT"]))
    crop_classifier, crop_classes = _load_efficientnet(paths["KGO_CROP_CLASSIFIER_CHECKPOINT"], device)
    full_classifier, full_classes = _load_efficientnet(paths["KGO_FULL_CLASSIFIER_CHECKPOINT"], device)
    transform = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    return detector, crop_classifier, crop_classes, full_classifier, full_classes, transform, device


def _select_platform_box(detector, image: Image.Image):
    results = detector(image, verbose=False)
    boxes = results[0].boxes
    if boxes is None or len(boxes) == 0:
        return None

    names = results[0].names
    target_id = next((idx for idx, name in names.items() if name == TARGET_DETECTION_CLASS), None)
    if target_id is None:
        return None

    for box in boxes:
        if int(box.cls[0]) == target_id:
            return box
    return None


def _predict_classifier(model, class_names: list[str], transform, image: Image.Image, device) -> tuple[str, float]:
    import torch

    tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(tensor)
        probabilities = torch.softmax(logits, dim=1)
        confidence, prediction = torch.max(probabilities, dim=1)
    return class_names[prediction.item()], float(confidence.item())


def predict_image(image_bytes: bytes) -> dict[str, Any]:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    detector, crop_model, crop_classes, full_model, full_classes, transform, device = load_models()

    box = _select_platform_box(detector, image)
    if box is None:
        annotated = _draw_overlay(image, "")
        return {
            "label": "",
            "confidence": 0.0,
            "bbox": None,
            "models": model_status(),
            "annotated_image": image_to_data_url(annotated),
        }

    x1, y1, x2, y2 = box.xyxy[0].tolist()
    crop = image.crop((x1, y1, x2, y2))
    crop_label, crop_confidence = _predict_classifier(crop_model, crop_classes, transform, crop, device)
    full_label, full_confidence = _predict_classifier(full_model, full_classes, transform, image, device)

    if crop_confidence >= full_confidence:
        label = crop_label
        confidence = crop_confidence
    else:
        label = "" if full_label == "kgo_none" else full_label
        confidence = full_confidence

    annotated = _draw_overlay(image, label)
    return {
        "label": label,
        "confidence": round(confidence, 4),
        "bbox": [round(value, 2) for value in (x1, y1, x2, y2)],
        "models": model_status(),
        "annotated_image": image_to_data_url(annotated),
    }


def predict_file(path: str | Path) -> dict[str, Any]:
    return predict_image(Path(path).read_bytes())
