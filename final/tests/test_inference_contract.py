from __future__ import annotations

from io import BytesIO

from PIL import Image

from app.services.inference import image_to_data_url


def test_image_to_data_url_returns_png_payload() -> None:
    image = Image.new("RGB", (8, 8), color=(1, 2, 3))

    payload = image_to_data_url(image)

    assert payload.startswith("data:image/png;base64,")
