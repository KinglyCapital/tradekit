import sqlite3
import os
from typing import final
import pandas as pd

from brokers.common.asset import AssetDataFrame
from brokers.common.bar import BarDataFrame
from brokers.common.repository import (
    MarketDataRepository,
    LoadBarsParams,
    SaveResult,
    SaveBarsParams,
)
from brokers.config import SqlLiteConfig


@final
class SQLiteMarketDataRepository(MarketDataRepository):
    def _connect_for_assets(self):
        """create a database connection to an SQLite database"""
        path = f"{SqlLiteConfig.SQLITE_PATH}"
        filename = "assets.db"
        os.makedirs(path, exist_ok=True)
        return sqlite3.connect(f"{path}/{filename}")

    def _connect_for_bars(self, symbol: str):
        """create a database connection to an SQLite database"""
        path = f"{SqlLiteConfig.SQLITE_PATH}/{self.broker.value}"
        filename = f"{symbol}.db"
        os.makedirs(path, exist_ok=True)
        return sqlite3.connect(f"{path}/{filename}")

    def save_assets(self, assets: AssetDataFrame) -> SaveResult:
        con = self._connect_for_assets()

        try:
            n = assets.to_sql(  # type: ignore
                name=self.broker.value,
                con=con,
                if_exists="replace",
                index=False,
                chunksize=1000,
            )
            return SaveResult(
                status="success",
                message=None,
                rows_affected=n if n else assets.shape[0],
            )
        except Exception as e:
            return SaveResult(status="error", message=str(e), rows_affected=0)
        finally:
            con.close()

    def load_assets(self) -> AssetDataFrame:
        con = self._connect_for_assets()
        query = f"SELECT * FROM {self.broker.value}"
        df = pd.read_sql(query, con=con)  # type: ignore
        return AssetDataFrame(df)

    def save_bars(self, params: SaveBarsParams) -> SaveResult:
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

    def load_bars(self, params: LoadBarsParams) -> BarDataFrame:
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
