"""Defines the Asset dataframe model."""

from typing import Optional, TypedDict
from pandera import DataFrameModel, Field  # type: ignore
from pandera.typing import Series, DataFrame

from brokers.common.enums import AssetClass, AssetStatus, Brokers


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

    broker: Series[str] = Field(isin=Brokers)
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


class AssetDict(TypedDict):
    """Defines the dictionary structure for an asset."""

    name: str
    symbol: str
    exchange: str
    broker: Brokers
    asset_class: AssetClass
    tradable: bool
    status: AssetStatus
    url_logo: Optional[str]
    pairs: Optional[str]
