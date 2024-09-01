"""Alpaca broker implementation."""

from brokers.config import ApiKeys


class AlpacaBroker:
    def __init__(self):
        self.api_key = ApiKeys.ALPACA_MARKET_DATA_KEY
        self.secret_key = ApiKeys.ALPACA_MARKET_DATA_SECRET
