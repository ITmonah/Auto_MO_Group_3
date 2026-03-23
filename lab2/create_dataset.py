#!/usr/bin/env python3
from pathlib import Path
import shutil

import kagglehub

ROOT = Path(__file__).resolve().parent
RAW_FILE = ROOT / "artifacts" / "raw" / "vgsales.csv"


def main() -> None:
    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not RAW_FILE.exists():
        dataset_dir = Path(kagglehub.dataset_download("gregorut/videogamesales"))
        source_file = next(dataset_dir.rglob("vgsales.csv"))
        shutil.copy2(source_file, RAW_FILE)

    print(RAW_FILE)


if __name__ == "__main__":
    main()
