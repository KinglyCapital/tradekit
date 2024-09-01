"""Contains the configuration for all brokers implementations."""

import os
from dotenv import dotenv_values

# Get the environment variables from the .env file (or .env.test).
config = dotenv_values()


class ApiKeys:
    """Contains the API keys for the Alpaca Broker."""

    ALPACA_MARKET_DATA_KEY = os.environ.get("ALPACA_MARKET_DATA_KEY")
    ALPACA_MARKET_DATA_SECRET = os.environ.get("ALPACA_MARKET_DATA_SECRET")


class SqlLiteConfig:
    """Contains the path to the SQL Lite database."""

    SQL_LITE_PATH = config.get("SQL_LITE_PATH")
