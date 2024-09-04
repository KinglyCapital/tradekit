from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from prices.core.asset import AssetDataFrame
from prices.core.bar import BarDataFrame
from prices.core.broker import Broker
from prices.core.timeframe import TimeFrame


@dataclass
class HistoricalPriceParams:
    """Defines the parameters for fetching prices for a symbol."""

    symbol: str
    """The symbol of the asset to fetch data for."""

    timeframe: TimeFrame
    """The time interval to fetch data for."""

    start: datetime
    """The start timestamp for the data to be fetched."""

    end: datetime | None
    """The end timestamp for the data to be fetched. If None, fetch data up to the current time."""

    limit: int | None
    """The maximum number of bars to fetch. If None, fetch all available bars."""

    def __init__(
        self,
        symbol: str,
        timeframe: TimeFrame,
        start: datetime,
        end: Optional[datetime] = None,
        limit: Optional[int] = None,
    ):
        self.symbol = symbol
        self.timeframe = timeframe
        self.start = start
        self.end = end
        self.limit = limit
        self._validate_params()

    def _validate_params(self):
        """Validates the fetch parameters. If the parameters are invalid, it raises a ValueError."""
        if self.start >= datetime.now():
            raise ValueError("Start date cannot be in the future.")

        if self.end and self.end >= datetime.now():
            raise ValueError("End date cannot be in the future.")

        if self.end and self.end <= self.start:
            raise ValueError("End date must be later than start date.")


class PriceFetcher(ABC):
    """Defines all methods for fetching price data."""

    def __init__(self, broker: Broker):
        self.broker = broker

    def __str__(self):
        return f"<{self.__class__.__name__}, {self.broker.value}>"

    @abstractmethod
    def assets(self) -> AssetDataFrame:
        """Returns a list of assets available for fetching price data."""
        ...

    @abstractmethod
    def historical(self, params: HistoricalPriceParams) -> BarDataFrame:
        """Returns data bars for a specific asset, time window and timeframe."""
        ...

    @abstractmethod
    def latest(self, symbol: str) -> BarDataFrame:
        """Returns the most recent data bar for a specific symbol."""
        ...
