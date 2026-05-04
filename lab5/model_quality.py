from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score


QUALITY_THRESHOLDS = {
    "mae": 0.55,
    "rmse": 0.70,
    "r2": 0.96,
}


@dataclass(frozen=True)
class RegressionDataset:
    name: str
    x: np.ndarray
    y: np.ndarray

    @property
    def features(self) -> np.ndarray:
        return self.x.reshape(-1, 1)


def generate_linear_dataset(
    *,
    name: str,
    seed: int,
    start: float,
    stop: float,
    size: int = 100,
    slope: float = 1.0,
    intercept: float = 0.0,
    noise_scale: float = 0.45,
    noisy_slice: slice | None = None,
    noisy_multiplier: float = 1.0,
) -> RegressionDataset:
    rng = np.random.default_rng(seed)
    x = np.linspace(start, stop, size)
    y = slope * x + intercept + rng.uniform(-noise_scale, noise_scale, size)

    if noisy_slice is not None:
        y[noisy_slice] *= noisy_multiplier

    return RegressionDataset(name=name, x=x, y=y)


def build_clean_datasets() -> dict[str, RegressionDataset]:
    return {
        "train_reference": generate_linear_dataset(
            name="train_reference",
            seed=7,
            start=0.0,
            stop=10.0,
            noise_scale=0.45,
        ),
        "clean_shifted_range": generate_linear_dataset(
            name="clean_shifted_range",
            seed=11,
            start=-5.0,
            stop=5.0,
            noise_scale=0.50,
        ),
        "clean_wide_range": generate_linear_dataset(
            name="clean_wide_range",
            seed=21,
            start=10.0,
            stop=20.0,
            noise_scale=0.35,
        ),
    }


def build_noisy_dataset() -> RegressionDataset:
    return generate_linear_dataset(
        name="noisy_outliers",
        seed=31,
        start=0.0,
        stop=10.0,
        noise_scale=0.45,
        noisy_slice=slice(25, 45),
        noisy_multiplier=2.0,
    )


def train_reference_model(dataset: RegressionDataset) -> LinearRegression:
    model = LinearRegression()
    model.fit(dataset.features, dataset.y)
    return model


def evaluate_model(model: LinearRegression, dataset: RegressionDataset) -> dict[str, float]:
    predictions = model.predict(dataset.features)
    return {
        "mae": float(mean_absolute_error(dataset.y, predictions)),
        "rmse": float(root_mean_squared_error(dataset.y, predictions)),
        "r2": float(r2_score(dataset.y, predictions)),
    }


def assert_quality(metrics: dict[str, float], thresholds: dict[str, float] | None = None) -> None:
    thresholds = thresholds or QUALITY_THRESHOLDS
    assert metrics["mae"] <= thresholds["mae"], (
        f"MAE={metrics['mae']:.3f} is above {thresholds['mae']:.3f}"
    )
    assert metrics["rmse"] <= thresholds["rmse"], (
        f"RMSE={metrics['rmse']:.3f} is above {thresholds['rmse']:.3f}"
    )
    assert metrics["r2"] >= thresholds["r2"], (
        f"R2={metrics['r2']:.3f} is below {thresholds['r2']:.3f}"
    )
