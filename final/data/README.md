# Data

Datasets are managed by DVC and are not stored in Git.

Expected layout after `dvc pull`:

```text
data/raw/
  kgo_empty/
    *.jpg|*.png
  kgo_full/
    *.jpg|*.png
```

Configure the real remote before pushing project data:

```bash
dvc remote modify dataset-remote url s3://<bucket>/<path>
dvc add data/raw
dvc push
```
