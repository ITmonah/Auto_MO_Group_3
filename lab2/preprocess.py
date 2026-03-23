#!/usr/bin/env python3
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
RAW_FILE = ROOT / "artifacts" / "raw" / "vgsales.csv"
PROCESSED_DIR = ROOT / "artifacts" / "processed"

NUMERIC_COLUMNS = ["Year", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
CATEGORICAL_COLUMNS = ["Platform", "Genre", "Publisher"]
COLUMNS = CATEGORICAL_COLUMNS + NUMERIC_COLUMNS + ["Global_Sales"]


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(RAW_FILE)[COLUMNS].drop_duplicates()

    for column in NUMERIC_COLUMNS + ["Global_Sales"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    for column in CATEGORICAL_COLUMNS:
        data[column] = data[column].astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA})

    data = data.dropna(subset=["Global_Sales"])
    data["target"] = (data["Global_Sales"] >= data["Global_Sales"].median()).astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        data[NUMERIC_COLUMNS + CATEGORICAL_COLUMNS],
        data["target"],
        test_size=0.2,
        random_state=42,
        stratify=data["target"],
    )

    medians = x_train[NUMERIC_COLUMNS].median()
    x_train[NUMERIC_COLUMNS] = x_train[NUMERIC_COLUMNS].fillna(medians)
    x_test[NUMERIC_COLUMNS] = x_test[NUMERIC_COLUMNS].fillna(medians)
    x_train[CATEGORICAL_COLUMNS] = x_train[CATEGORICAL_COLUMNS].fillna("Unknown")
    x_test[CATEGORICAL_COLUMNS] = x_test[CATEGORICAL_COLUMNS].fillna("Unknown")

    scaler = StandardScaler()
    x_train[NUMERIC_COLUMNS] = scaler.fit_transform(x_train[NUMERIC_COLUMNS])
    x_test[NUMERIC_COLUMNS] = scaler.transform(x_test[NUMERIC_COLUMNS])

    x_train = pd.get_dummies(x_train, columns=CATEGORICAL_COLUMNS, dtype=int).sort_index(axis=1)
    x_test = pd.get_dummies(x_test, columns=CATEGORICAL_COLUMNS, dtype=int).reindex(
        columns=x_train.columns,
        fill_value=0,
    )

    train_data = x_train.copy()
    train_data["target"] = y_train.to_numpy()

    test_data = x_test.copy()
    test_data["target"] = y_test.to_numpy()

    train_data.to_csv(PROCESSED_DIR / "train_processed.csv", index=False)
    test_data.to_csv(PROCESSED_DIR / "test_processed.csv", index=False)

    print(PROCESSED_DIR)


if __name__ == "__main__":
    main()
