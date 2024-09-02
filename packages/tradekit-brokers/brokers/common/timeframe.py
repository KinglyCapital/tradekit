"""Defines the TimeFrame and TimeFrameUnit classes for specifying time intervals."""

from enum import Enum
from typing import Literal


TimeFrameLiteral = Literal["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]


class TimeFrameUnit(str, Enum):
    """Quantity of time used as unit"""

    Minute = "Min"
    Hour = "Hour"
    Day = "Day"
    Week = "Week"
    Month = "Month"


class TimeFrame:
    """A time interval specified in multiples of defined units (minute, day, etc)"""

    amount_value: int
    """amount_value (int): The number of multiples of the TimeFrameUnit interval"""

    unit_value: TimeFrameUnit
    """unit_value (TimeFrameUnit): The base unit that is used to measure the TimeFrame"""

    value: str
    """value (str): The string representation of the TimeFrame"""

    def __init__(self, amount: int, unit: TimeFrameUnit) -> None:
        self.validate_timeframe(amount, unit)
        self.amount_value = amount
        self.unit_value = unit
        self.value = f"{self.amount_value}{self.unit_value}"

    @staticmethod
    def validate_timeframe(amount: int, unit: TimeFrameUnit):
        """Validates the amount value against the TimeFrameUnit value for consistency

        Args:
            amount (int): The number of multiples of unit
            unit (TimeFrameUnit): The base unit of time interval the TimeFrame is measured by

        Raises:
            ValueError: Raised if the values of amount and unit are not consistent with each other
        """
        if amount <= 0:
            raise ValueError("Amount must be a positive integer value.")

        if unit == TimeFrameUnit.Minute and amount > 59:
            raise ValueError(
                "Second or Minute units can only be " + "used with amounts between 1-59."
            )

        if unit == TimeFrameUnit.Hour and amount > 23:
            raise ValueError("Hour units can only be used with amounts 1-23")

        if unit in (TimeFrameUnit.Day, TimeFrameUnit.Week) and amount != 1:
            raise ValueError("Day and Week units can only be used with amount 1")

        if unit == TimeFrameUnit.Month and amount not in (1, 2, 3, 6, 12):
            raise ValueError("Month units can only be used with amount 1, 2, 3, 6 and 12")

    @property
    def name_value(self) -> str:
        """The name of the TimeFrame. For example, '1m' for 1 minute."""

        match self.unit_value:
            case TimeFrameUnit.Minute:
                return f"{self.amount_value}m"
            case TimeFrameUnit.Hour:
                return f"{self.amount_value}h"
            case TimeFrameUnit.Day:
                return f"{self.amount_value}d"
            case TimeFrameUnit.Week:
                return f"{self.amount_value}w"
            case TimeFrameUnit.Month:
                return f"{self.amount_value}M"


class TimeFramePresets:
    """A list of predefined TimeFrame values"""

    TimeframeMonthly = TimeFrame(1, TimeFrameUnit.Month)
    """TimeFrame: A time interval of 1 month"""

    TimeframeWeekly = TimeFrame(1, TimeFrameUnit.Week)
    """TimeFrame: A time interval of 1 week"""

    TimeframeDaily = TimeFrame(1, TimeFrameUnit.Day)
    """TimeFrame: A time interval of 1 day"""

    Timeframe4H = TimeFrame(4, TimeFrameUnit.Hour)
    """TimeFrame: A time interval of 4 hours"""

    Timeframe2H = TimeFrame(2, TimeFrameUnit.Hour)
    """TimeFrame: A time interval of 2 hours"""

    Timeframe1H = TimeFrame(1, TimeFrameUnit.Hour)
    """TimeFrame: A time interval of 1 hour"""

    Timeframe30Min = TimeFrame(30, TimeFrameUnit.Minute)
    """TimeFrame: A time interval of 30 minutes"""

    Timeframe15Min = TimeFrame(15, TimeFrameUnit.Minute)
    """TimeFrame: A time interval of 15 minutes"""

    Timeframe5Min = TimeFrame(5, TimeFrameUnit.Minute)
    """TimeFrame: A time interval of 5 minutes"""

    Timeframe1Min = TimeFrame(1, TimeFrameUnit.Minute)
    """TimeFrame: A time interval of 1 minute"""
