"""Defines the TimeFrame and TimeFrameUnit classes for specifying time intervals."""

from enum import Enum


class _TimeFrameUnit(str, Enum):
    """Quantity of time used as unit."""

    Minute = "Min"
    Hour = "Hour"
    Day = "Day"
    Week = "Week"
    Month = "Month"


class TimeFrame:
    """A time interval specified in multiples of defined units (minute, day, etc)."""

    amount_value: int
    """The number of multiples of the _TimeFrameUnit interval."""

    unit_value: _TimeFrameUnit
    """The base unit that is used to measure the TimeFrame."""

    value: str
    """The string representation of the TimeFrame."""

    def __init__(self, amount: int, unit: _TimeFrameUnit) -> None:
        self.validate_timeframe(amount, unit)
        self.amount_value = amount
        self.unit_value = unit
        self.value = f"{self.amount_value}{self.unit_value}"

    @staticmethod
    def validate_timeframe(amount: int, unit: _TimeFrameUnit):
        """Validates the amount value against the TimeFrameUnit value for consistency."""
        if amount <= 0:
            raise ValueError("Amount must be a positive integer value.")

        if unit == _TimeFrameUnit.Minute and amount > 59:
            raise ValueError(
                "Second or Minute units can only be " + "used with amounts between 1-59."
            )

        if unit == _TimeFrameUnit.Hour and amount > 23:
            raise ValueError("Hour units can only be used with amounts 1-23")

        if unit in (_TimeFrameUnit.Day, _TimeFrameUnit.Week) and amount != 1:
            raise ValueError("Day and Week units can only be used with amount 1")

        if unit == _TimeFrameUnit.Month and amount not in (1, 2, 3, 6, 12):
            raise ValueError("Month units can only be used with amount 1, 2, 3, 6 and 12")

    @property
    def name_value(self) -> str:
        """The name of the TimeFrame. For example, '1m' for 1 minute."""

        match self.unit_value:
            case _TimeFrameUnit.Minute:
                return f"{self.amount_value}m"
            case _TimeFrameUnit.Hour:
                return f"{self.amount_value}h"
            case _TimeFrameUnit.Day:
                return f"{self.amount_value}d"
            case _TimeFrameUnit.Week:
                return f"{self.amount_value}w"
            case _TimeFrameUnit.Month:
                return f"{self.amount_value}M"


class TFPreset:
    """A list of predefined TimeFrame values."""

    Tf_M = TimeFrame(1, _TimeFrameUnit.Month)
    """TimeFrame: A time interval of 1 month."""

    Tf_W = TimeFrame(1, _TimeFrameUnit.Week)
    """TimeFrame: A time interval of 1 week."""

    Tf_D = TimeFrame(1, _TimeFrameUnit.Day)
    """TimeFrame: A time interval of 1 day."""

    Tf_4h = TimeFrame(4, _TimeFrameUnit.Hour)
    """TimeFrame: A time interval of 4 hours."""

    Tf_2h = TimeFrame(2, _TimeFrameUnit.Hour)
    """TimeFrame: A time interval of 2 hours."""

    Tf_1h = TimeFrame(1, _TimeFrameUnit.Hour)
    """TimeFrame: A time interval of 1 hour."""

    Tf_30m = TimeFrame(30, _TimeFrameUnit.Minute)
    """TimeFrame: A time interval of 30 minutes."""

    Tf_15m = TimeFrame(15, _TimeFrameUnit.Minute)
    """TimeFrame: A time interval of 15 minutes."""

    Tf_5m = TimeFrame(5, _TimeFrameUnit.Minute)
    """TimeFrame: A time interval of 5 minutes."""

    Tf_1m = TimeFrame(1, _TimeFrameUnit.Minute)
    """TimeFrame: A time interval of 1 minute."""
