from __future__ import annotations
from collections import deque
from typing import Any, AsyncIterator
import asyncio
import numpy as np
from dl_real_time_drilling.app.logging import LOGGER
from dl_real_time_drilling.models.base import FeatureMaker, ModelRunner


async def run_stream(
    source: AsyncIterator[dict[str, Any]],
    features: FeatureMaker,
    model: ModelRunner,
    window: int = 64,
) -> AsyncIterator[dict[str, Any]]:
    buffer: deque[dict[str, Any]] = deque(maxlen=window)
    async for row in source:
        buffer.append(row)
        if len(buffer) == window:
            # Convert to simple feature dict; adapt as needed
            rows = {k: np.array([r[k] for r in buffer]) for k in buffer[0].keys()}
            feats = features.transform(rows)
            preds = model.predict(feats)
            LOGGER.info("⚙️ streamed inference")
            yield preds
        await asyncio.sleep(0)



