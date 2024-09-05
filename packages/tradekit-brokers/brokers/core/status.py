from dataclasses import dataclass
from datetime import datetime


@dataclass
class Status:
    """
    The Status class is a data structure that holds information about the current
    state of the market.

    For example:

        {
            "timestamp": "2024-09-05T10:42:10.36924109-04:00",
            "is_open": true,
            "next_open": "2024-09-06T09:30:00-04:00",
            "next_close": "2024-09-05T16:00:00-04:00"
        }
    """

    timestamp: datetime
    is_open: bool
    next_open: datetime
    next_close: datetime

    def __repr__(self):
        return f"Clock({self.timestamp}, {self.is_open}, {self.next_open}, {self.next_close})"

    def __str__(self):
        return f"Clock({self.timestamp}, {self.is_open}, {self.next_open}, {self.next_close})"
