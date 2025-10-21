from __future__ import annotations
import polars as pl


def basic_time_features(df: pl.DataFrame, window: int = 64) -> pl.DataFrame:
    # Example rolling stats; adjust columns as needed
    numeric_cols = [c for c, dt in zip(df.columns, df.dtypes) if dt.is_numeric()]
    out = df.clone()
    for col in numeric_cols:
        out = out.with_columns(
            pl.col(col).rolling_mean(window_size=window).alias(f"{col}_mean_{window}"),
            pl.col(col).diff().alias(f"{col}_diff"),
        )
    return out



