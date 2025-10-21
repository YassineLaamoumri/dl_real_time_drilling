from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import polars as pl

from dl_real_time_drilling.app.logging import LOGGER


@dataclass(frozen=True)
class TimeCleanConfig:
    """Configuration for cleaning time-indexed drilling telemetry.

    Attributes:
        timestamp_column: Canonical timestamp column name.
        required_numeric_columns: Columns expected to be numeric; will be coerced.
        rename_map: Optional map of input->canonical column names.
        plausible_ranges: Optional bounds used to clip sensor values.
        drop_negative_rop: If True, force non-negative ROP.
        deduplicate: If True, drop duplicate timestamps keeping the last.
        sort: If True, sort by timestamp ascending.
        fill_method: Strategy to fill missing numeric values.
                     one of {"ffill_bfill", "median", "none"}.
    """

    timestamp_column: str = "timestamp"
    required_numeric_columns: tuple[str, ...] = (
        "hookload",
        "rpm",
        "torque",
        "flow",
        "spm",
        "standpipe_pressure",
        "wob",
        "bit_depth",
        "hole_depth",
        "rop",
    )
    rename_map: dict[str, str] = field(default_factory=dict)
    plausible_ranges: dict[str, tuple[float, float]] = field(default_factory=dict)
    drop_negative_rop: bool = True
    deduplicate: bool = True
    sort: bool = True
    fill_method: str = "ffill_bfill"


def _ensure_timestamp(df: pl.DataFrame, ts_col: str) -> pl.DataFrame:
    if ts_col not in df.columns:
        raise ValueError(f"Missing timestamp column: {ts_col}")
    # Cast to pl.Datetime if possible; accept strings or ints (epoch ms/s)
    # Try ISO8601 parse first; if fails, try epoch milliseconds, then seconds
    out = df.with_columns(
        pl.col(ts_col)
        .str.strptime(pl.Datetime, strict=False, ambiguous="earliest", time_unit=None)
        .fill_null(
            pl.col(ts_col)
            .cast(pl.Int64, strict=False)
            .map_elements(lambda v: v // 1000 if v and abs(v) > 10_000_000_000 else v)
            .cast(pl.Datetime, time_unit="s", strict=False)
        )
        .alias(ts_col)
    )
    if out.select(pl.col(ts_col).is_null().any()).item():
        raise ValueError("Failed to parse timestamp column to datetime")
    return out


def _rename_columns(df: pl.DataFrame, rename_map: dict[str, str]) -> pl.DataFrame:
    if not rename_map:
        return df
    missing_sources = [c for c in rename_map if c not in df.columns]
    if missing_sources:
        LOGGER.warning(
            f"⚠️ rename_map contains columns missing from input: {missing_sources}"
        )
    return df.rename({k: v for k, v in rename_map.items() if k in df.columns})


def _coerce_numeric(df: pl.DataFrame, numeric_cols: Iterable[str]) -> pl.DataFrame:
    present = [c for c in numeric_cols if c in df.columns]
    out = df.with_columns([pl.col(c).cast(pl.Float64, strict=False).alias(c) for c in present])
    return out


def _clip_ranges(df: pl.DataFrame, ranges: dict[str, tuple[float, float]]) -> pl.DataFrame:
    out = df
    for col, (lo, hi) in ranges.items():
        if col in out.columns:
            out = out.with_columns(pl.col(col).clip_min(lo).clip_max(hi))
    return out


def _fill_missing(df: pl.DataFrame, method: str, numeric_cols: Iterable[str]) -> pl.DataFrame:
    cols = [c for c in numeric_cols if c in df.columns]
    if not cols or method == "none":
        return df
    if method == "median":
        medians = df.select([pl.col(c).median().alias(c) for c in cols]).row(0)
        replacements = dict(zip(cols, medians))
        return df.with_columns([pl.col(c).fill_null(replacements[c]) for c in cols])
    if method == "ffill_bfill":
        # Forward then backward fill within each column
        out = df.with_columns([pl.col(c).forward_fill().alias(c) for c in cols])
        out = out.with_columns([pl.col(c).backward_fill().alias(c) for c in cols])
        return out
    raise ValueError(f"Unknown fill method: {method}")


def _drop_dupes_and_sort(df: pl.DataFrame, ts_col: str, deduplicate: bool, sort: bool) -> pl.DataFrame:
    out = df
    if deduplicate:
        out = out.unique(subset=[ts_col], keep="last")
    if sort:
        out = out.sort(ts_col)
    return out


def clean_time_log(df: pl.DataFrame, cfg: TimeCleanConfig | None = None) -> pl.DataFrame:
    """Clean a time-indexed telemetry `pl.DataFrame` into a normalized form.

    Steps:
        1) Optional renaming of columns into canonical names.
        2) Timestamp parsing to timezone-naive UTC `Datetime`.
        3) Numeric coercion for required telemetry columns.
        4) Optional clipping to plausible sensor ranges.
        5) Optional ROP non-negativity enforcement.
        6) Missing value handling according to `fill_method`.
        7) De-duplication and sorting by timestamp.

    Raises:
        ValueError: When required columns are missing or timestamp cannot be parsed.
    """

    cfg = cfg or TimeCleanConfig()

    LOGGER.info("🧽 starting time-log cleaning")
    out = _rename_columns(df, cfg.rename_map)

    # Validate presence of required columns (ignore missing numeric for now, we coerce later)
    missing_required = [c for c in (cfg.timestamp_column,) if c not in out.columns]
    if missing_required:
        raise ValueError(f"Missing required columns: {missing_required}")

    out = _ensure_timestamp(out, cfg.timestamp_column)

    # Coerce numeric and handle missing values
    out = _coerce_numeric(out, cfg.required_numeric_columns)

    # Clip to plausible ranges if provided
    if cfg.plausible_ranges:
        out = _clip_ranges(out, cfg.plausible_ranges)

    # Enforce non-negative ROP when requested
    if cfg.drop_negative_rop and "rop" in out.columns:
        out = out.with_columns(pl.when(pl.col("rop") < 0).then(0.0).otherwise(pl.col("rop")).alias("rop"))

    # Fill missing values
    out = _fill_missing(out, cfg.fill_method, cfg.required_numeric_columns)

    # De-duplicate and sort by timestamp
    out = _drop_dupes_and_sort(out, cfg.timestamp_column, cfg.deduplicate, cfg.sort)

    LOGGER.info("✅ time-log cleaning complete")
    return out


__all__ = [
    "TimeCleanConfig",
    "clean_time_log",
]



