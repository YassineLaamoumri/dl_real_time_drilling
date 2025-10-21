from __future__ import annotations

import polars as pl

from dl_real_time_drilling.dataprep.cleaning import TimeCleanConfig, clean_time_log


def test_clean_time_log_parses_timestamp_and_coerces_numeric() -> None:
    df = pl.DataFrame(
        {
            "timestamp": ["2024-01-01T00:00:00Z", "2024-01-01T00:00:01Z", "2024-01-01T00:00:02Z"],
            "rop": [1, -2, None],
            "rpm": [120, 130, 140],
        }
    )
    cfg = TimeCleanConfig(required_numeric_columns=("rpm", "rop"))
    out = clean_time_log(df, cfg)
    assert out.schema["timestamp"].is_datetime()
    assert out.select(pl.col("rop").min()).item() >= 0
    assert out.select(pl.col("rpm").median()).item() == 130


def test_clean_time_log_dedup_and_sort() -> None:
    df = pl.DataFrame(
        {
            "timestamp": ["2024-01-01T00:00:01Z", "2024-01-01T00:00:00Z", "2024-01-01T00:00:01Z"],
            "rop": [1.0, 2.0, 3.0],
        }
    )
    out = clean_time_log(df)
    ts = out.select("timestamp").to_series()
    assert ts.is_sorted()
    assert out.height == 2


