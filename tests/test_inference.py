from __future__ import annotations
import numpy as np
import pytest
from dl_real_time_drilling.serving.inference_mlflow import OnnxRunner


def test_runner_predict_signature(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyRunner:
        def __init__(self, *_: object, **__: object) -> None:
            pass

        def predict(self, x: np.ndarray) -> np.ndarray:
            return x

    # monkeypatch the class for unit test without MLflow
    from dl_real_time_drilling.serving import inference_mlflow as mod

    monkeypatch.setattr(mod, "OnnxRunner", DummyRunner, raising=True)
    r = mod.OnnxRunner("ignored")
    out = r.predict(np.array([[1, 2, 3]], dtype=np.float32))
    assert out.shape == (1, 3)

