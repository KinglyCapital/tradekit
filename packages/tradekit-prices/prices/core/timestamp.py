"""Defines the class to represent a timestamp which is a datetime with a UTC timezone."""

import pandas as pd


class Timestamp(pd.DatetimeTZDtype):
    """Defines a timestamp in the format of a datetime64[ns] with a UTC."""

    def __init__(self):
        super().__init__(unit="ns", tz="UTC")

    def __str__(self):
        return "Timestamp(datetime64[ns, UTC])"
