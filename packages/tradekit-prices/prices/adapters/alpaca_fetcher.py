"""Alpaca broker implementation."""

from typing import cast, final

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models import BarSet
from alpaca.data.requests import StockBarsRequest, StockLatestBarRequest
from alpaca.data.timeframe import TimeFrame as AlpacaTimeFrame

from prices.adapters.config import AlpacaApiKeys
from prices.core.bar import BarDataFrame
from prices.core.broker import Broker
from prices.ports.price_fetcher import HistoricalPriceParams, PriceFetcher


@final
class AlpacaPriceFetcher(PriceFetcher):
    """Alpaca price fetcher adapter."""

    def __init__(self):
        super().__init__(broker=Broker.ALPACA)

        historical_data_client = StockHistoricalDataClient(
            api_key=AlpacaApiKeys.ALPACA_MARKET_DATA_KEY,
            secret_key=AlpacaApiKeys.ALPACA_MARKET_DATA_SECRET,
            raw_data=False,
        )

        self._get_stock_bars = historical_data_client.get_stock_bars
        self._get_stock_latest_bar = historical_data_client.get_stock_latest_bar

    def historical(self, params: HistoricalPriceParams) -> BarDataFrame:
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
        response = self._get_stock_bars(request)

        # Normalize the data to the BarDataFrame format.
        df = cast(BarSet, response).df
        df = df.reset_index()
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")

        return BarDataFrame(df)

    def latest(self, symbol: str) -> BarDataFrame:
        """Fetches the latest bar from the Alpaca API."""
        request = StockLatestBarRequest(symbol_or_symbols=symbol)
        response = self._get_stock_latest_bar(request)

        # Normalize the data to the BarDataFrame format.
        bar = response.get(symbol)
        df = pd.DataFrame([vars(bar)])
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")

        return BarDataFrame(df)
