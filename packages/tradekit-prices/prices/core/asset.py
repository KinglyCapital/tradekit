"""Defines the Asset dataframe model."""

from enum import Enum

from pandera import DataFrameModel, Field  # type: ignore
from pandera.typing import DataFrame, Series

from prices.core.broker import Broker


class AssetClass(str, Enum):
    """List of asset classes."""

    EQUITY = "Equity"
    CRYPTO = "Crypto"
    FOREX = "Forex"


class AssetStatus(str, Enum):
    """
    Represents the status of an asset. This status can be 'Active' or 'Inactive' if the asset is
    available for trading or not in specific broker. Some brokers may have different status values.
    And sometimes the asset may be temporarily unavailable for trading by the exchange itself.
    """

    ACTIVE = "Active"
    INACTIVE = "Inactive"


class _AssetModel(DataFrameModel):
    """Defines the data of an asset that can be traded by the broker."""

    name: Series[str]
    """The name of the asset. For example, for equity, this could be 'Apple Inc' for Apple Inc.
    or 'Bitcoin' for Bitcoin."""

    symbol: Series[str]
    """A symbol that represents the asset. For example, for equity, this could be 'AAPL' for
    Apple Inc or 'BTC' for Bitcoin."""

    exchange: Series[str]
    """The exchange in which the asset is traded. For example, for equity, this could be 'NASDAQ'
    or 'NYSE'. Or for cryptocurrency, this could be 'Binance' or 'Coinbase'."""

    broker: Series[str] = Field(isin=Broker)
    """The broker that provides access to the asset."""

    asset_class: Series[str] = Field(isin=AssetClass)
    """The type of asset. Can be 'equity', 'crypto', or 'forex'."""

    tradable: Series[bool]
    """Indicates whether the asset is currently active and available for trading."""

    status: Series[str] = Field(isin=AssetStatus)
    """The asset status in the broker."""

    url_logo: Series[str] = Field(nullable=True)
    """URL to the logo of the asset. This can be used to display the logo of the asset in a
    user interface."""

    pairs: Series[str] = Field(nullable=True)
    """A list of trading pairs that include this asset. This is useful for defining trading pairs
    in the context of cryptocurrency exchanges or forex trading."""


AssetDataFrame = DataFrame[_AssetModel]
"""A DataFrame type that contains assets."""
