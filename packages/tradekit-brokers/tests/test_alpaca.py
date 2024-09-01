"""Test for Alpaca broker."""

from brokers.alpaca import AlpacaBroker


def test_alpaca_broker():
    """Test AlpacaBroker class."""
    alpaca_broker = AlpacaBroker()

    print(alpaca_broker.api_key)
    print(alpaca_broker.secret_key)
