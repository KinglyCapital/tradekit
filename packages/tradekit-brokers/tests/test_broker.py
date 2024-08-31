"""Broker unit test module."""

from brokers.broker import Broker


def test_broker():
    broker = Broker()

    assert broker is not None
