import os
import sqlite3
from typing import final

import pandas as pd

from prices.adapters.config import SqlLiteConfig
from prices.core.bar import BarDataFrame
from prices.ports.price_repository import LoadParams, PriceRepository, SaveParams, SaveResult


@final
class SQLiteMarketDataRepository(PriceRepository):
    def _connect_for_bars(self, symbol: str):
        """Create a database connection to an SQLite database"""
        path = f"{SqlLiteConfig.SQLITE_PATH}/{self.broker.value}"
        filename = f"{symbol}.db"
        os.makedirs(path, exist_ok=True)
        return sqlite3.connect(f"{path}/{filename}")

    def save(self, params: SaveParams) -> SaveResult:
        con = self._connect_for_bars(symbol=params.symbol)

        try:
            n = params.bars.to_sql(  # type: ignore
                name=f"tf_{params.timeframe.name_value}",
                con=con,
                if_exists="replace",
                index=False,
            )
            return SaveResult(
                status="success",
                message=None,
                rows_affected=n if n else params.bars.shape[0],
            )
        except Exception as e:
            return SaveResult(status="error", message=str(e), rows_affected=0)
        finally:
            con.close()

    def load(self, params: LoadParams) -> BarDataFrame:
        con = self._connect_for_bars(symbol=params.symbol)
        try:
            table = f"tf_{params.timeframe.name_value}"

            query = f"SELECT * FROM {table}"
            if params.start_date is not None:
                query += f" WHERE timestamp >= '{params.start_date}'"
            if params.end_date is not None:
                query += f" AND timestamp <= '{params.end_date}'"

            df = pd.read_sql(query, con)  # type: ignore
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)  # type: ignore

            return BarDataFrame(df)
        finally:
            con.close()
