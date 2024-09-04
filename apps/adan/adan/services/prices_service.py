from adan.common.utils import format_datetime, to_response
from prices.adapters.alpaca_fetcher import AlpacaPriceFetcher
from prices.adapters.sqlite_repository import SQLitePriceRepository
from prices.core.broker import Broker
from prices.core.timeframe import TFPreset
from prices.ports.price_repository import LoadHistoricalParams


class PricesService:
    def __init__(self):
        self.repository = SQLitePriceRepository(Broker.ALPACA)
        self.fetcher = AlpacaPriceFetcher()

    def get_assets(self):
        assets = self.repository.load_assets()
        return to_response(assets)

    def get_historical(self):
        df = self.repository.load_historical(
            LoadHistoricalParams(symbol="AAPL", timeframe=TFPreset.Tf_4h, limit=100)
        )
        df = format_datetime(df)

        return to_response(df)
