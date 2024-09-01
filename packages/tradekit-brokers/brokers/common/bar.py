"""Defines the Bar dataframe shape for storing OHLCV data."""

from pandera.typing import Series, DataFrame
from pandera import DataFrameModel
import pandas as pd


class Bar(DataFrameModel):
    """Dataframe with columns representing the OHLCV (Open, High, Low, Close, Volume) data of a
    financial asset in a specific time frame."""

    symbol: Series[str]
    """The asset symbol of the bar."""

    timestamp: Series[pd.DatetimeTZDtype]
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


BarDataFrame = DataFrame[Bar]
"""A DataFrame type that contains bars."""
