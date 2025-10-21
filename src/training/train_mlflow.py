from __future__ import annotations
from pathlib import Path
from typing import Any
import mlflow
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import lightning as L
from dl_real_time_drilling.app.logging import LOGGER
from dl_real_time_drilling.models.lightning_module import LitModel
from dl_real_time_drilling.models.onnx_export import export_onnx


class SimpleDataset(Dataset):
    def __init__(self, X: torch.Tensor, y: torch.Tensor) -> None:
        self.X = X
        self.y = y

    def __len__(self) -> int:
        return self.X.size(0)

    def __getitem__(self, i: int):
        return self.X[i], self.y[i]


def train_with_mlflow(cfg: dict[str, Any]) -> None:
    mlflow.set_tracking_uri(cfg["tracking_uri"])
    mlflow.set_experiment(cfg["experiment_name"])
    if "registry_uri" in cfg:
        mlflow.set_registry_uri(cfg["registry_uri"])
    mlflow.pytorch.autolog(log_models=False)

    X = torch.randn(2048, 32)
    y = torch.randn(2048, 1)
    ds = SimpleDataset(X, y)
    dl = DataLoader(ds, batch_size=64, shuffle=True, num_workers=2)
    model = LitModel(nn.Sequential(nn.Linear(32, 64), nn.ReLU(), nn.Linear(64, 1)))

    LOGGER.info("🚀 starting training")
    with mlflow.start_run():
        mlflow.log_params({"lr": 1e-3, "batch_size": 64, "window": 64})

        trainer = L.Trainer(max_epochs=3, accelerator="auto", devices="auto")
        trainer.fit(model, dl)
        LOGGER.info("✅ training done")

        onnx_path = export_onnx(model.net, Path("artifacts/model.onnx"))
        mlflow.onnx.log_model(onnx_model=str(onnx_path), artifact_path="onnx-model")


