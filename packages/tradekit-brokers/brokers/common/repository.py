from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from brokers.common.asset import AssetDataFrame
from brokers.common.bar import BarDataFrame
from brokers.common.enums import Brokers
from brokers.common.timeframe import TimeFrame


@dataclass
class LoadBarsParams:
    symbol: str
    timeframe: TimeFrame
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


@dataclass
class SaveBarsParams:
    symbol: str
    timeframe: TimeFrame
    bars: BarDataFrame


@dataclass
class SaveResult:
    status: Literal["success", "error"]
    message: Optional[str]
    rows_affected: int


class MarketDataRepository(ABC):
    def __init__(self, broker: Brokers) -> None:
        self.broker = broker

    @abstractmethod
    def save_assets(self, assets: AssetDataFrame) -> SaveResult: ...

    @abstractmethod
    def load_assets(self) -> AssetDataFrame: ...

    @abstractmethod
    def save_bars(self, params: SaveBarsParams) -> SaveResult: ...

    @abstractmethod
    def load_bars(self, params: LoadBarsParams) -> BarDataFrame: ...
