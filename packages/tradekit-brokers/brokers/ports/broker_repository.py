from abc import ABC, abstractmethod
from typing import List

from brokers.core.broker import Broker
from brokers.core.calendar import Calendar


class BrokerRepository(ABC):
    def __init__(self, broker: Broker):
        self.broker = broker

    @abstractmethod
    def save_calendar(self, calendar: List[Calendar]) -> None: ...
