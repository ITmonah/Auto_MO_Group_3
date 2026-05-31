from __future__ import annotations

from app.model_registry import ensure_models, model_status


def main() -> None:
    ensure_models(download=True)
    for model in model_status():
        print(f"{model['name']}: {model['path']}")


if __name__ == "__main__":
    main()
