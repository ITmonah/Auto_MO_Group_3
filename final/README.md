# KGO Fill Detection

Финальный проект: конвейер машинного обучения для data-продукта в виде FastAPI Web/API приложения. Приложение принимает изображение, находит платформу `kgo_platform` YOLO-моделью и классифицирует заполненность EfficientNet-классификаторами.

## Что входит

- `app/` - FastAPI приложение и inference-сервис.
- `scripts/download_models.py` - загрузка весов из отдельного model registry.
- `scripts/validate_data.py` - проверка качества датасета.
- `tests/` - unit-тесты и тесты data quality логики.
- `dvc.yaml`, `.dvc/config` - DVC-конвейер и удаленное хранилище датасетов.
- `Dockerfile` - сборка итогового приложения в Docker-образ.
- `Jenkinsfile` - CI/CD: установка, `dvc pull`, data quality, unit tests, docker build.

## Модели

Файлы `.pt` и `.pth` не хранятся в этом репозитории. Они должны быть доступны из отдельного репозитория или release-хранилища:

- `Yolo26s_kgo.pt`
- `best_efficientnet_v2_s_kgo.pth`
- `best_efficientnet_for_full.pth`

Для автоматической загрузки задайте:

```bash
export MODEL_REGISTRY_BASE_URL=https://raw.githubusercontent.com/<org>/<models-repo>/main
python scripts/download_models.py
```

Также можно указать конкретные пути:

```bash
export KGO_YOLO_CHECKPOINT=/path/to/Yolo26s_kgo.pt
export KGO_CROP_CLASSIFIER_CHECKPOINT=/path/to/best_efficientnet_v2_s_kgo.pth
export KGO_FULL_CLASSIFIER_CHECKPOINT=/path/to/best_efficientnet_for_full.pth
```

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/download_models.py
uvicorn app.main:app --reload
```

Web UI: `http://localhost:8000`

API:

```bash
curl -F "image=@sample.jpg" http://localhost:8000/api/predict
```

## DVC

Датасет не хранится в Git. Ожидаемая структура после `dvc pull`:

```text
data/raw/
  kgo_empty/
  kgo_full/
```

Настройка реального хранилища:

```bash
dvc remote modify dataset-remote url s3://<bucket>/<path>
dvc add data/raw
dvc push
```

Проверка данных:

```bash
python scripts/validate_data.py --dataset data/raw --classes kgo_empty kgo_full --min-images-per-class 1
```

## Ветки и версии

Рекомендуемый процесс разработки:

- фичи приложения: `feature/<name>`;
- изменения пайплайна или модели: `model/<name>`;
- версии датасета: `data/<dataset-version>`;
- релизные версии приложения: Git tags `vX.Y.Z`.

После обновления данных выполняется `dvc add data/raw`, коммитится `.dvc`-метаданные и выполняется `dvc push`. Код и DVC-метаданные проходят review в pull request.

## CI/CD

`Jenkinsfile` выполняет:

1. Установку зависимостей.
2. `dvc pull` для синхронизации датасета.
3. Data quality tests.
4. Unit tests через `pytest`.
5. Сборку Docker-образа.

## Docker

```bash
docker build -t kgo-fill-detection .
docker run --rm -p 8000:8000 -e MODEL_REGISTRY_BASE_URL=$MODEL_REGISTRY_BASE_URL kgo-fill-detection
```
