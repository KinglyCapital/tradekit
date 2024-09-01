"""Test for Alpaca broker."""

from datetime import datetime
import pytest

from brokers.alpaca import AlpacaMarketData
from brokers.common.broker import MarketDataBarsParams
from brokers.common.timeframe import TimeFramePresets


class TestAlpacaMarketData:
    """Test Alpaca Market Data implementation."""

    @pytest.fixture
    def alpaca(self):
        """Test AlpacaBroker class."""
        return AlpacaMarketData()

    def test_alpaca_limit(self, alpaca: AlpacaMarketData):
        bars = alpaca.bars(
            MarketDataBarsParams(
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeDaily,
                start=datetime(2021, 1, 1),
                limit=5,
            )
        )

        assert bars.shape[0] == 5

    def test_alpaca_no_limit(self, alpaca: AlpacaMarketData):
        bars = alpaca.bars(
            MarketDataBarsParams(
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeMonthly,
                start=datetime(2023, 1, 1),
            )
        )

        assert bars.shape[0] > 12

    def test_alpaca_date_range(self, alpaca: AlpacaMarketData):
        bars = alpaca.bars(
            MarketDataBarsParams(
                symbol="AAPL",
                timeframe=TimeFramePresets.TimeframeDaily,
                start=datetime(2024, 8, 26),
                end=datetime(2024, 8, 31),
            )
        )

        assert bars.shape[0] == 5
