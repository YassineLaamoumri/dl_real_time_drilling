from __future__ import annotations
from pathlib import Path
import numpy as np
import onnxruntime as ort
import mlflow
from mlflow import artifacts
from dl_real_time_drilling.app.logging import LOGGER


class OnnxRunner:
    def __init__(self, model_name: str, stage: str = "Staging") -> None:
        model_dir = artifacts.download_artifacts(artifact_uri=f"models:/{model_name}/{stage}")
        onnx_fp = Path(model_dir) / "data" / "model.onnx"
        self.session = ort.InferenceSession(str(onnx_fp), providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        LOGGER.info(f"🤖 loaded {model_name}@{stage}")

    def predict(self, x: np.ndarray) -> np.ndarray:
        out = self.session.run([self.output_name], {self.input_name: x})[0]
        LOGGER.info("📡 inference ok")
        return out



