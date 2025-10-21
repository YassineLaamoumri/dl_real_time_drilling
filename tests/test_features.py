from __future__ import annotations
import polars as pl
from dl_real_time_drilling.dataprep.transforms import basic_time_features


def test_basic_time_features_adds_columns() -> None:
    df = pl.DataFrame({"a": [1, 2, 3, 4], "b": [10, 20, 30, 40]})
    out = basic_time_features(df, window=2)
    assert any(c.startswith("a_mean_") for c in out.columns)
    assert "a_diff" in out.columns

