"""Defines all interfaces related to brokers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


from brokers.common.bar import BarDataFrame
from brokers.common.timeframe import TimeFrame


@dataclass
class MarketDataBarsParams:
    """Defines the parameters for fetching bars from the broker."""

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
            raise ValueError("Start date cannot be in the future")

        if self.end and self.end >= datetime.now():
            raise ValueError("End date cannot be in the future")

        if self.end and self.end <= self.start:
            raise ValueError("End date must be later than start date")


class MarketData(ABC):
    """Defines all methods exposed by a broker for fetching market data."""

    # @abstractmethod
    # def assets(self):
    #     """Returns a list of assets available for trading on the broker."""
    #     pass

    @abstractmethod
    def bars(self, params: MarketDataBarsParams) -> BarDataFrame:
        """Returns data bars for a specific asset, time window and timeframe."""
        pass

    # @abstractmethod
    # def snapshot(self, symbol: str) -> Snapshoot:
    #     """Returns a snapshot of the asset."""
    #     pass


class Account(ABC):
    """Defines all methods exposed by a broker for fetching account information."""

    @abstractmethod
    def account(self): ...

    @abstractmethod
    def positions(self): ...

    @abstractmethod
    def orders(self): ...

    @abstractmethod
    def portfolio(self): ...

    @abstractmethod
    def watchlist(self): ...


class Trading(ABC):
    """Defines all methods exposed by a broker for trading."""

    @abstractmethod
    def place_order(self): ...

    @abstractmethod
    def cancel_order(self): ...

    @abstractmethod
    def order_status(self): ...

    @abstractmethod
    def order_executions(self): ...

    @abstractmethod
    def order_history(self): ...

    @abstractmethod
    def trades(self): ...

    @abstractmethod
    def trade_history(self): ...


class Broker(MarketData, Account, Trading):
    """Defines all methods exposed by a broker."""

    pass
