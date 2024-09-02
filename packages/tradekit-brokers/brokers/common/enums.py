from enum import Enum


class Brokers(str, Enum):
    """
    List of supported brokers.
    """

    ALPACA = "Alpaca"
    BINANCE = "Binance"

    def __str__(self) -> str:
        return str(self.value)


class AssetClass(str, Enum):
    """
    List of asset classes.
    """

    EQUITY = "Equity"
    CRYPTO = "Crypto"
    FOREX = "Forex"

    def __str__(self) -> str:
        return str(self.value)


class AssetStatus(str, Enum):
    """
    Represents the status of an asset. This status can be 'Active' or 'Inactive' if the asset is
    available for trading or not in specific broker. Some brokers may have different status values.
    And sometimes the asset may be temporarily unavailable for trading by the exchange itself.
    """

    ACTIVE = "Active"
    INACTIVE = "Inactive"

    def __str__(self) -> str:
        return str(self.value)
