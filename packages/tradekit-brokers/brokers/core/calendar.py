from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Calendar:
    """
    Calendar data for a specific trading venue.

    For example:

        {
            "date": "1970-01-02",
            "open": "09:30",
            "close": "16:00",
        }
    """

    date: date
    open: datetime
    close: datetime
