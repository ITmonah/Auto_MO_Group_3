#!/usr/bin/env python3
from pathlib import Path
import json
import pickle

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

ROOT = Path(__file__).resolve().parent
TEST_FILE = ROOT / "artifacts" / "processed" / "test_processed.csv"
MODEL_FILE = ROOT / "artifacts" / "models" / "model.pkl"
METRICS_FILE = ROOT / "artifacts" / "reports" / "evaluation_metrics.json"


def main() -> None:
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

    test_data = pd.read_csv(TEST_FILE)

    with MODEL_FILE.open("rb") as file:
        payload = pickle.load(file)

    feature_columns = payload["feature_columns"]
    predictions = payload["model"].predict(test_data.reindex(columns=feature_columns, fill_value=0))

    metrics = {
        "accuracy": float(accuracy_score(test_data["target"], predictions)),
        "precision": float(precision_score(test_data["target"], predictions, zero_division=0)),
        "recall": float(recall_score(test_data["target"], predictions, zero_division=0)),
        "f1": float(f1_score(test_data["target"], predictions, zero_division=0)),
    }

    METRICS_FILE.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(metrics)


if __name__ == "__main__":
    main()
