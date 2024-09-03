"""Test for Alpaca broker."""

from datetime import datetime
import pytest

from brokers.alpaca_broker import AlpacaMarketData
from brokers.common.broker import MarketDataBarsParams
from brokers.common.timeframe import TimeFramePresets


@pytest.fixture
def alpaca() -> AlpacaMarketData:
    """Test AlpacaBroker class."""
    return AlpacaMarketData()


class TestAlpacaMarketData:
    """Test Alpaca Market Data implementation."""

    def test_alpaca_assets(self, alpaca: AlpacaMarketData):
        assets = alpaca.assets()
        assert assets.shape[0] > 0

    def test_alpaca_bars_limit(self, alpaca: AlpacaMarketData):
        bars = alpaca.bars(
            MarketDataBarsParams(
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeDaily,
                start=datetime(2021, 1, 1),
                limit=5,
            )
        )

        assert bars.shape[0] == 5

    def test_alpaca_bars_no_limit(self, alpaca: AlpacaMarketData):
        bars = alpaca.bars(
            MarketDataBarsParams(
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeMonthly,
                start=datetime(2023, 1, 1),
            )
        )

        assert bars.shape[0] > 12

    def test_alpaca_bars_date_range(self, alpaca: AlpacaMarketData):
        bars = alpaca.bars(
            MarketDataBarsParams(
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeDaily,
                start=datetime(2024, 8, 26),
                end=datetime(2024, 8, 31),
            )
        )

        assert bars.shape[0] == 5
