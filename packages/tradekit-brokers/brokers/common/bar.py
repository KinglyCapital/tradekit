"""Defines the Bar dataframe shape for storing OHLCV data."""

from pandera.typing import Series, DataFrame
from pandera import DataFrameModel
import pandas as pd


class BarTimestamp(pd.DatetimeTZDtype):
    """Defines a timestamp for a bar in the format of a datetime64[ns] with a UTC."""

    def __init__(self):
        super().__init__(unit="ns", tz="UTC")

    def __str__(self):
        return "BarTimestamp(datetime64[ns, UTC])"


class _BarModel(DataFrameModel):
    """Defines OHLCV (Open, High, Low, Close, Volume) data of a financial asset in a
    specific time frame."""

    symbol: Series[str]
    """The asset symbol of the bar."""

    timestamp: Series[BarTimestamp]  # type: ignore
    """The timestamp of the bar, in seconds since the Unix epoch."""

    open: Series[float]
    """The opening price of the bar."""

    high: Series[float]
    """The highest price of the bar."""

    low: Series[float]
    """The lowest price of the bar."""

    close: Series[float]
    """The closing price of the bar."""

    volume: Series[float]
    """The volume of the bar."""

    vwap: Series[float]
    """The volume-weighted average price of the bar."""


BarDataFrame = DataFrame[_BarModel]
"""A DataFrame type that contains bars."""
