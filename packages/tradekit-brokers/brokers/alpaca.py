"""Alpaca broker implementation."""

from typing import cast, final

from brokers.config import ApiKeys
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame as AlpacaTimeFrame
from alpaca.data.models import BarSet

from brokers.common.bar import BarDataFrame
from brokers.common.broker import MarketData, MarketDataBarsParams


@final
class AlpacaMarketData(MarketData):
    """Alpaca broker implementation for fetching market data."""

    def __init__(self):
        self._client = StockHistoricalDataClient(
            api_key=ApiKeys.ALPACA_MARKET_DATA_KEY,
            secret_key=ApiKeys.ALPACA_MARKET_DATA_SECRET,
            raw_data=False,
        )

    def bars(self, params: MarketDataBarsParams) -> BarDataFrame:
        """Fetches bars from the Alpaca API."""
        request = StockBarsRequest(
            symbol_or_symbols=params.symbol,
            timeframe=AlpacaTimeFrame(
                params.timeframe.amount_value,
                params.timeframe.unit_value,
            ),
            start=params.start,
            end=params.end,
            limit=params.limit,
        )
        df = cast(BarSet, self._client.get_stock_bars(request)).df
        df = df.reset_index()
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")
        return BarDataFrame(df)
