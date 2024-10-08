"""Contains the configuration for all brokers implementations."""

import os
from dotenv import load_dotenv

# Get the environment variables from the .env file (or .env.test).
load_dotenv()


class ApiKeys:
    """Contains the API keys for the Alpaca Broker."""

    ALPACA_MARKET_DATA_KEY = os.environ.get("ALPACA_MARKET_DATA_KEY")
    ALPACA_MARKET_DATA_SECRET = os.environ.get("ALPACA_MARKET_DATA_SECRET")


class SqlLiteConfig:
    """Contains the path to the SQL Lite database."""

    SQLITE_PATH = os.environ.get("SQLITE_PATH")
