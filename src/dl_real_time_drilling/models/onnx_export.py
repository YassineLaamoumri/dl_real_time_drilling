from __future__ import annotations
from pathlib import Path
import torch
import torch.nn as nn
from dl_real_time_drilling.app.logging import LOGGER


def export_onnx(model: nn.Module, out_path: Path, input_dim: int = 32, opset: int = 17) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dummy = torch.randn(1, input_dim)
    torch.onnx.export(
        model,
        dummy,
        out_path,
        input_names=["input"],
        output_names=["output"],
        opset_version=opset,
        dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
    )
    LOGGER.info(f"📦 onnx exported: {out_path}")
    return out_path



