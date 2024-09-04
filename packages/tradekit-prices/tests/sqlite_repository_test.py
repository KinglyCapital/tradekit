from datetime import datetime

import pytest

from prices.adapters.alpaca_fetcher import AlpacaPriceFetcher
from prices.adapters.sqlite_repository import SQLitePriceRepository
from prices.core.asset import AssetDataFrame
from prices.core.bar import BarDataFrame
from prices.core.broker import Broker
from prices.core.timeframe import TFPreset
from prices.ports.price_fetcher import HistoricalPriceParams
from prices.ports.price_repository import LoadHistoricalParams, SaveHistoricalParams


class TestSQLiteRepository:
    """Test SQLite Price Repository adapter."""

    @pytest.fixture
    def repository(self) -> SQLitePriceRepository:
        return SQLitePriceRepository(Broker.ALPACA)

    @pytest.fixture
    def assets(self) -> AssetDataFrame:
        return AlpacaPriceFetcher().assets()

    @pytest.fixture
    def historical(self) -> BarDataFrame:
        return AlpacaPriceFetcher().historical(
            HistoricalPriceParams(
                symbol="META",
                timeframe=TFPreset.Tf_D,
                start=datetime(2023, 1, 1),
                limit=10,
            )
        )

    def test_save_assets(self, repository: SQLitePriceRepository, assets: AssetDataFrame):
        result = repository.save_assets(assets)

        assert result.status == "success"
        assert result.rows_affected == assets.shape[0]

    def test_save_historical(self, repository: SQLitePriceRepository, historical: BarDataFrame):
        result = repository.save_historical(
            SaveHistoricalParams(
                symbol="META",
                timeframe=TFPreset.Tf_D,
                bars=historical,
            )
        )

        assert result.status == "success"
        assert result.rows_affected == historical.shape[0]

    def test_load_assets(self, repository: SQLitePriceRepository):
        assets = repository.load_assets()
        assert assets.shape[0] > 0

    def test_load_historical(self, repository: SQLitePriceRepository):
        bars = repository.load_historical(
            LoadHistoricalParams(
                symbol="META",
                timeframe=TFPreset.Tf_D,
                start=datetime(2023, 1, 1),
            )
        )

        assert bars.shape[0] == 10

    def test_load_historical_limit(self, repository: SQLitePriceRepository):
        bars = repository.load_historical(
            LoadHistoricalParams(
                symbol="META",
                timeframe=TFPreset.Tf_D,
                limit=5,
            )
        )

        assert bars.shape[0] == 5
