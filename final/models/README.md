# Model files

This directory is intentionally excluded from Git. Put local copies here only for development.

Required files:

- `Yolo26s_kgo.pt`
- `best_efficientnet_v2_s_kgo.pth`
- `best_efficientnet_for_full.pth`

In CI/CD and Docker, set `MODEL_REGISTRY_BASE_URL` to a separate repository or release asset base URL that contains these files. Individual paths can also be overridden with `KGO_YOLO_CHECKPOINT`, `KGO_CROP_CLASSIFIER_CHECKPOINT`, and `KGO_FULL_CLASSIFIER_CHECKPOINT`.
