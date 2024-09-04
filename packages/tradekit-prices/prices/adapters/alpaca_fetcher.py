"""Alpaca price fetcher implementation."""

from typing import List, cast, final

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.models import BarSet
from alpaca.data.requests import StockBarsRequest, StockLatestBarRequest
from alpaca.data.timeframe import TimeFrame as AlpacaTimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass as AlpacaAssetClass
from alpaca.trading.enums import AssetStatus as AlpacaAssetStatus
from alpaca.trading.models import Asset as AlpacaAsset
from alpaca.trading.requests import GetAssetsRequest

from prices.adapters.config import AlpacaApiKeys
from prices.core.asset import AssetClass, AssetDataFrame, AssetStatus
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

        trading_client = TradingClient(
            api_key=AlpacaApiKeys.ALPACA_MARKET_DATA_KEY,
            secret_key=AlpacaApiKeys.ALPACA_MARKET_DATA_SECRET,
            raw_data=False,
        )

        self._get_all_assets = trading_client.get_all_assets
        self._get_stock_bars = historical_data_client.get_stock_bars
        self._get_stock_latest_bar = historical_data_client.get_stock_latest_bar

    def assets(self) -> AssetDataFrame:
        """Fetches assets from the Alpaca API."""

        request = GetAssetsRequest(asset_class=AlpacaAssetClass.US_EQUITY)
        assets_list = cast(List[AlpacaAsset], self._get_all_assets(request))

        # Normalize the data to the AssetDataFrame format.
        assets = [
            {
                "name": asset.name if asset.name else "",
                "symbol": asset.symbol,
                "exchange": asset.exchange.value,
                "broker": Broker.ALPACA,
                "tradable": asset.tradable,
                "asset_class": AssetClass.EQUITY,
                "status": (
                    AssetStatus.ACTIVE
                    if asset.status == AlpacaAssetStatus.ACTIVE
                    else AssetStatus.INACTIVE
                ),
                # TODO: In the future, we can add a logo URL here (alpaca broker API).
                # Ref: https://docs.alpaca.markets/reference/get-v1beta1-logos-symbol-1
                "url_logo": None,
                "pairs": None,
            }
            for asset in assets_list
        ]

        df = pd.DataFrame(assets)
        return AssetDataFrame(df)

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
