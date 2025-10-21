from __future__ import annotations
from fastapi import FastAPI
import numpy as np
from dl_real_time_drilling.app.logging import LOGGER
from dl_real_time_drilling.serving.inference_mlflow import OnnxRunner


app = FastAPI(title="dl-serving")
runner: OnnxRunner | None = None


@app.on_event("startup")
def startup() -> None:
    global runner
    try:
        runner = OnnxRunner("drilling-rt", stage="Staging")
        LOGGER.info("🚀 api started")
    except Exception as exc:  # noqa: BLE001
        LOGGER.error(f"🔥 failed to init model: {exc}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/infer")
def infer(payload: dict) -> dict:
    assert runner is not None, "Model not loaded"
    x = np.asarray(payload["input"], dtype=np.float32)
    out = runner.predict(x)
    LOGGER.info("📡 request served")
    return {"output": out.tolist()}



