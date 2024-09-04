from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from prices.core.asset import AssetDataFrame
from prices.core.bar import BarDataFrame
from prices.core.broker import Broker
from prices.core.timeframe import TimeFrame


@dataclass
class SaveHistoricalParams:
    """Defines the parameters for saving historical price data."""

    symbol: str
    timeframe: TimeFrame
    bars: BarDataFrame


@dataclass
class LoadHistoricalParams:
    """Defines the parameters for loading historical price data."""

    symbol: str
    timeframe: TimeFrame
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    limit: Optional[int] = None


@dataclass
class SaveResult:
    """Defines the result of saving historical price data."""

    status: Literal["success", "error"]
    message: Optional[str]
    rows_affected: int


class PriceRepository(ABC):
    """
    Interface Port for a price repository that saves and loads historical price data for a
    specific `Broker`.
    """

    def __init__(self, broker: Broker) -> None:
        self.broker = broker

    @abstractmethod
    def save_assets(self, assets: AssetDataFrame) -> SaveResult:
        """Save assets data."""
        ...

    @abstractmethod
    def save_historical(self, params: SaveHistoricalParams) -> SaveResult:
        """Save historical price data."""
        ...

    @abstractmethod
    def load_assets(self) -> AssetDataFrame:
        """Load assets data."""
        ...

    @abstractmethod
    def load_historical(self, params: LoadHistoricalParams) -> BarDataFrame:
        """Load historical price data."""
        ...
