import os
from datetime import date, timedelta
from typing import List, cast, final

from alpaca.trading.client import TradingClient
from alpaca.trading.models import Calendar as AlpacaCalendar
from alpaca.trading.requests import GetCalendarRequest
from dotenv import load_dotenv

from brokers.core.broker import Broker
from brokers.core.calendar import Calendar
from brokers.ports.broker_info import BrokerInfo

# Get the environment variables from the .env file (or .env.test).
load_dotenv()

ALPACA_MARKET_DATA_KEY = os.environ.get("ALPACA_MARKET_DATA_KEY")
ALPACA_MARKET_DATA_SECRET = os.environ.get("ALPACA_MARKET_DATA_SECRET")


@final
class AlpacaBrokerInfo(BrokerInfo):
    def __init__(self):
        super().__init__(broker=Broker.ALPACA)

        client = TradingClient(
            api_key=ALPACA_MARKET_DATA_KEY,
            secret_key=ALPACA_MARKET_DATA_SECRET,
            raw_data=False,
        )

        self._get_calendar = client.get_calendar
        self._clock = client.get_clock

    def calendar(self) -> List[Calendar]:
        calendar = cast(List[AlpacaCalendar], self._get_calendar())

        return [
            Calendar(
                date=day.date,
                open=day.open,
                close=day.close,
            )
            for day in calendar
        ]

    def next_open(self) -> Calendar:
        today = date.today()
        end = today + timedelta(days=10)  # Just to ensure we get the next open date.

        calendar = cast(
            List[AlpacaCalendar],
            self._get_calendar(GetCalendarRequest(start=today, end=end)),
        )

        return Calendar(
            date=calendar[1].date,
            open=calendar[1].open,
            close=calendar[1].close,
        )
