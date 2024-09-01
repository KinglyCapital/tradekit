"""Defines the Pair class."""

from dataclasses import dataclass


@dataclass
class Pair:
    """Defines the basic information of a pair of assets that can be traded. This is useful for
    defining trading pairs in the context of cryptocurrency exchanges or forex trading."""

    base: str
    """The base asset of the pair. For example, for the pair BTC/USD, the base asset is BTC."""

    quote: str
    """The quote asset of the pair. For example, for the pair BTC/USD, the quote asset is USD."""

    def __str__(self) -> str:
        return f"{self.base}/{self.quote}"
