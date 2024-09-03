from datetime import datetime
import pytest

from brokers.alpaca_broker import AlpacaMarketData
from brokers.common.asset import AssetDataFrame
from brokers.common.bar import BarDataFrame
from brokers.common.broker import MarketDataBarsParams
from brokers.common.repository import LoadBarsParams, SaveBarsParams
from brokers.common.timeframe import TimeFramePresets
from brokers.common.enums import Brokers
from brokers.repositories.sqlite_repository import SQLiteMarketDataRepository

LIMIT_BARS = 72


class TestSQLiteRepository:
    @pytest.fixture
    def assets(self) -> AssetDataFrame:
        """Test AlpacaBroker class."""
        return AlpacaMarketData().assets()

    @pytest.fixture
    def bars(self) -> BarDataFrame:
        return AlpacaMarketData().bars(
            MarketDataBarsParams(
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeDaily,
                start=datetime(2018, 1, 1),
                limit=LIMIT_BARS,
            )
        )

    @pytest.fixture
    def repository(self) -> SQLiteMarketDataRepository:
        """Test SQLiteRepository class."""
        return SQLiteMarketDataRepository(Brokers.ALPACA)

    def test_save_assets(self, assets: AssetDataFrame, repository: SQLiteMarketDataRepository):
        result = repository.save_assets(assets)
        assert result.status == "success"
        assert result.rows_affected == assets.shape[0]
        assert result.message is None

    def load_assets(self, repository: SQLiteMarketDataRepository):
        assets = repository.load_assets()
        assert assets.shape[0] > 0

    def test_save_bars(self, bars: BarDataFrame, repository: SQLiteMarketDataRepository):
        result = repository.save_bars(
            SaveBarsParams(
                bars=bars,
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeDaily,
            )
        )
        assert result.status == "success"
        assert result.rows_affected == bars.shape[0]
        assert result.message is None

    def test_load_bars(self, repository: SQLiteMarketDataRepository):

        # Gel All.
        bars = repository.load_bars(
            LoadBarsParams(
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeDaily,
            )
        )

        assert bars.shape[0] == LIMIT_BARS

        # Get a range.
        bars = repository.load_bars(
            LoadBarsParams(
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeDaily,
                start_date=datetime(2018, 1, 1),
                end_date=datetime(2018, 1, 10),
            )
        )

        assert bars.shape[0] == 6
