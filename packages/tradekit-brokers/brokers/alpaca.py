"""Alpaca broker implementation."""

import pandas as pd
from typing import List, cast, final
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame as AlpacaTimeFrame
from alpaca.data.models import BarSet
from alpaca.trading import TradingClient
from alpaca.trading.models import Asset as AlpacaAsset
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass as AlpacaAssetClass, AssetStatus as AlpacaAssetStatus

from brokers.common.asset import AssetDataFrame, AssetDict
from brokers.common.broker import MarketData, MarketDataBarsParams
from brokers.common.bar import BarDataFrame
from brokers.common.enums import AssetClass, AssetStatus, Brokers
from brokers.config import ApiKeys


@final
class AlpacaMarketData(MarketData):
    """Alpaca broker implementation for fetching market data."""

    def __init__(self):
        """Initializes the Alpaca broker"""

        historical_data_client = StockHistoricalDataClient(
            api_key=ApiKeys.ALPACA_MARKET_DATA_KEY,
            secret_key=ApiKeys.ALPACA_MARKET_DATA_SECRET,
            raw_data=False,
        )

        trading_client = TradingClient(
            api_key=ApiKeys.ALPACA_MARKET_DATA_KEY,
            secret_key=ApiKeys.ALPACA_MARKET_DATA_SECRET,
            raw_data=False,
        )

        # Mapping only necessary methods to avoid exposing the entire client.
        self._get_all_assets = trading_client.get_all_assets
        self._get_stock_bars = historical_data_client.get_stock_bars

    def assets(self) -> AssetDataFrame:
        """Fetches assets from the Alpaca API."""
        request = GetAssetsRequest(asset_class=AlpacaAssetClass.US_EQUITY)
        assets_list = cast(List[AlpacaAsset], self._get_all_assets(request))

        # Normalize the data to the AssetDataFrame format.
        assets = [
            AssetDict(
                name=asset.name if asset.name else "",
                symbol=asset.symbol,
                exchange=asset.exchange.value,
                broker=Brokers.ALPACA,
                tradable=asset.tradable,
                asset_class=AssetClass.EQUITY,
                status=(
                    AssetStatus.ACTIVE
                    if asset.status == AlpacaAssetStatus.ACTIVE
                    else AssetStatus.INACTIVE
                ),
                # TODO: In the future, we can add a logo URL here (alpaca broker API).
                # Ref: https://docs.alpaca.markets/reference/get-v1beta1-logos-symbol-1
                url_logo=None,
                pairs=None,
            )
            for asset in assets_list
        ]

        df = pd.DataFrame(assets)
        return AssetDataFrame(df)

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
        df = cast(BarSet, self._get_stock_bars(request)).df
        df = df.reset_index()
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")
        return BarDataFrame(df)
