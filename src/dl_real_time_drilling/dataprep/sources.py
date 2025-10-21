from __future__ import annotations
from pathlib import Path
from typing import Iterable
import polars as pl


def load_time_csvs(paths: Iterable[Path]) -> pl.DataFrame:
    frames: list[pl.DataFrame] = []
    for p in paths:
        frames.append(pl.read_csv(p))
    return pl.concat(frames, how="vertical_relaxed")


def load_depth_csvs(paths: Iterable[Path]) -> pl.DataFrame:
    frames: list[pl.DataFrame] = []
    for p in paths:
        frames.append(pl.read_csv(p))
    return pl.concat(frames, how="vertical_relaxed")



