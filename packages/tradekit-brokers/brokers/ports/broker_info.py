from abc import ABC, abstractmethod
from typing import List

from brokers.core.broker import Broker
from brokers.core.calendar import Calendar


class BrokerInfo(ABC):
    def __init__(self, broker: Broker):
        self.broker = broker

    @abstractmethod
    def calendar(self) -> List[Calendar]: ...

    @abstractmethod
    def next_open(self) -> Calendar: ...

    # @abstractmethod
    # def status(self) -> Status: ...
