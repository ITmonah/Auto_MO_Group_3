#!/usr/bin/env python3
from __future__ import annotations

import argparse
from io import StringIO
from pathlib import Path

import pandas as pd


BASE_DATASET = """PassengerId,Pclass,Sex,Age
1,3,male,22
2,1,female,38
3,3,female,26
4,1,female,35
5,3,male,
6,3,male,35
7,1,male,54
8,3,male,2
9,3,female,27
10,2,female,14
11,3,female,4
12,1,male,
"""


def load_base_dataset() -> pd.DataFrame:
    return pd.read_csv(StringIO(BASE_DATASET))


def create_base_dataset(output_path: Path) -> None:
    df = load_base_dataset()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Created base dataset at: {output_path}")


def fill_missing_age(dataset_path: Path) -> None:
    df = pd.read_csv(dataset_path)
    mean_age = df["Age"].mean()
    df["Age"] = df["Age"].fillna(mean_age)
    df.to_csv(dataset_path, index=False)
    print(f"Filled missing Age values with mean={mean_age:.2f}")


def one_hot_encode_sex(dataset_path: Path) -> None:
    df = pd.read_csv(dataset_path)
    encoded = pd.get_dummies(df["Sex"], prefix="Sex", dtype=int)
    df = pd.concat([df.drop(columns=["Sex"]), encoded], axis=1)
    df.to_csv(dataset_path, index=False)
    print(f"Applied one-hot encoding to Sex in: {dataset_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create and transform the lab4 Titanic dataset."
    )
    parser.add_argument(
        "action",
        choices=["create-base", "fill-age", "encode-sex"],
        help="Dataset action to perform.",
    )
    parser.add_argument(
        "--dataset-path",
        default=Path("lab4/data/titanic.csv"),
        type=Path,
        help="Path to the tracked CSV dataset.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_path = args.dataset_path

    if args.action == "create-base":
        create_base_dataset(dataset_path)
    elif args.action == "fill-age":
        fill_missing_age(dataset_path)
    else:
        one_hot_encode_sex(dataset_path)


if __name__ == "__main__":
    main()
