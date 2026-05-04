from __future__ import annotations

from statistics import mean

import pytest

from lab5.model_quality import (
    QUALITY_THRESHOLDS,
    assert_quality,
    build_clean_datasets,
    build_noisy_dataset,
    evaluate_model,
    train_reference_model,
)


CLEAN_DATASETS = build_clean_datasets()
MODEL = train_reference_model(CLEAN_DATASETS["train_reference"])
CLEAN_METRICS = {
    name: evaluate_model(MODEL, dataset)
    for name, dataset in CLEAN_DATASETS.items()
}
NOISY_METRICS = evaluate_model(MODEL, build_noisy_dataset())


@pytest.mark.parametrize("dataset_name", CLEAN_METRICS.keys())
def test_clean_datasets_meet_quality_requirements(dataset_name: str) -> None:
    assert_quality(CLEAN_METRICS[dataset_name], QUALITY_THRESHOLDS)


def test_noisy_dataset_breaks_quality_requirements() -> None:
    with pytest.raises(AssertionError):
        assert_quality(NOISY_METRICS, QUALITY_THRESHOLDS)


def test_noisy_dataset_is_much_worse_than_clean_datasets() -> None:
    average_clean_mae = mean(metrics["mae"] for metrics in CLEAN_METRICS.values())
    minimum_clean_r2 = min(metrics["r2"] for metrics in CLEAN_METRICS.values())

    assert NOISY_METRICS["mae"] > average_clean_mae * 3
    assert NOISY_METRICS["r2"] < minimum_clean_r2 - 0.10
