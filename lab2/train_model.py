#!/usr/bin/env python3
from pathlib import Path
import pickle

import pandas as pd
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parent
TRAIN_FILE = ROOT / "artifacts" / "processed" / "train_processed.csv"
MODEL_FILE = ROOT / "artifacts" / "models" / "model.pkl"


def main() -> None:
    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)

    train_data = pd.read_csv(TRAIN_FILE)
    feature_columns = [column for column in train_data.columns if column != "target"]

    model = LogisticRegression(max_iter=1000)
    model.fit(train_data[feature_columns], train_data["target"])

    with MODEL_FILE.open("wb") as file:
        pickle.dump({"model": model, "feature_columns": feature_columns}, file)

    print(MODEL_FILE)


if __name__ == "__main__":
    main()
