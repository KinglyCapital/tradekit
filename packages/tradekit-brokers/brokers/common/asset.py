"""Defines the Asset and Pair classes."""

from dataclasses import dataclass
from typing import Literal

# Define type aliases for the Asset class.
AssetClass = Literal["stock", "crypto", "forex"]
"""Type alias for the asset class. Can be 'stock', 'crypto', or 'forex'."""

# Define type aliases for the currency in which the asset is traded.
AssetCurrency = Literal["USD", "CLP"]
"""Type alias for the currency in which the asset is traded. Can be 'USD' for US dollars or 'CLP'"""


@dataclass
class Asset:
    """Defines the basic information of an asset that can be traded."""

    name: str
    """The name of the asset. For example, for stocks, this could be 'Apple Inc' for Apple Inc.
    or 'Bitcoin' for Bitcoin."""

    symbol: str
    """A symbol that represents the asset. For example, for stocks, this could be 'AAPL' for
    Apple Inc or 'BTC' for Bitcoin."""

    currency: AssetCurrency
    """The currency in which the asset is traded. For example, for stocks, this could be 'USD' for
    US dollars or 'CLP' for Chilean pesos."""

    exchange: str
    """The exchange in which the asset is traded. For example, for stocks, this could be 'NASDAQ'
    or 'NYSE' for US stocks."""

    broker: str
    """The broker that provides access to the asset. For example, 'Alpaca' or 'Binance'."""

    asset_class: AssetClass
    """The type of asset. Can be 'stock', 'crypto', or 'forex'."""

    url_logo: str
    """URL to the logo of the asset. This can be used to display the logo of the asset in a
    user interface."""

    def __str__(self) -> str:
        return f"{self.symbol} ({self.name})"


@dataclass
class Pair:
    """Defines the basic information of a pair of assets that can be traded. This is useful for
    defining trading pairs in the context of cryptocurrency exchanges or forex trading."""

    base: Asset
    """The base asset of the pair. For example, for the pair BTC/USD, the base asset is BTC."""

    quote: Asset
    """The quote asset of the pair. For example, for the pair BTC/USD, the quote asset is USD."""

    def __str__(self) -> str:
        return f"{self.base.symbol}/{self.quote.symbol}"
