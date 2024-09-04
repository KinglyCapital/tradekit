from datetime import datetime

import pytest

from prices.adapters.alpaca_fetcher import AlpacaPriceFetcher
from prices.core.timeframe import TFPreset
from prices.ports.price_fetcher import HistoricalPriceParams


class TestAlpacaMarketData:
    """Test Alpaca Market Data implementation."""

    @pytest.fixture
    def alpaca(self) -> AlpacaPriceFetcher:
        return AlpacaPriceFetcher()

    def test_assets(self, alpaca: AlpacaPriceFetcher):
        assets = alpaca.assets()
        print(assets)
        assert assets.shape[0] > 0

    def test_historical_limit(self, alpaca: AlpacaPriceFetcher):
        bars = alpaca.historical(
            HistoricalPriceParams(
                symbol="AAPL",
                timeframe=TFPreset.Tf_D,
                start=datetime(2021, 1, 1),
                limit=5,
            )
        )

        assert bars.shape[0] == 5

    def test_alpaca_bars_no_limit(self, alpaca: AlpacaPriceFetcher):
        bars = alpaca.historical(
            HistoricalPriceParams(
                symbol="AAPL",
                timeframe=TFPreset.Tf_M,
                start=datetime(2023, 1, 1),
            )
        )

        assert bars.shape[0] > 12

    def test_alpaca_bars_date_range(self, alpaca: AlpacaPriceFetcher):
        bars = alpaca.historical(
            HistoricalPriceParams(
                symbol="AAPL",
                timeframe=TFPreset.Tf_D,
                start=datetime(2024, 8, 26),
                end=datetime(2024, 8, 31),
            )
        )

        assert bars.shape[0] == 5

    def test_latest(self, alpaca: AlpacaPriceFetcher):
        bar = alpaca.latest("AAPL")
        assert bar.shape[0] > 0
