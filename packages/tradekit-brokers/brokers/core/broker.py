from enum import Enum


class Broker(str, Enum):
    """List of supported brokers."""

    ALPACA = "Alpaca"
    BINANCE = "Binance"

    def __str__(self) -> str:
        return str(self.value)
