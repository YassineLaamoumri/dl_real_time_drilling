from __future__ import annotations
from typing import Protocol
import numpy as np


class FeatureMaker(Protocol):
    def transform(self, rows: dict[str, np.ndarray]) -> dict[str, np.ndarray]: ...


class ModelRunner(Protocol):
    def predict(self, features: dict[str, np.ndarray]) -> dict[str, np.ndarray]: ...



