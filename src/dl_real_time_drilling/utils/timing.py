from __future__ import annotations
from contextlib import contextmanager
import time
from typing import Iterator
from dl_real_time_drilling.app.logging import LOGGER


@contextmanager
def time_block(name: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        dur_ms = (time.perf_counter() - start) * 1000
        LOGGER.info(f"⏱️ {name} took {dur_ms:.2f}ms")



