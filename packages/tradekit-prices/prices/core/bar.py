"""Defines the Bar Dataframe for OHLCV data."""

from pandera import DataFrameModel
from pandera.typing import DataFrame, Series

from prices.core.timestamp import Timestamp


class _BarDataFrameModel(DataFrameModel):
    """Defines OHLCV (Open, High, Low, Close, Volume) data of a financial asset in a
    specific time frame."""

    symbol: Series[str]
    """The asset symbol of the bar."""

    timestamp: Series[Timestamp]  # type: ignore
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


BarDataFrame = DataFrame[_BarDataFrameModel]
"""A DataFrame type that contains bars."""
