import os
import sqlite3
from typing import final

import pandas as pd

from prices.adapters.config import SqlLiteConfig
from prices.core.asset import AssetDataFrame
from prices.core.bar import BarDataFrame
from prices.ports.price_repository import (
    LoadHistoricalParams,
    PriceRepository,
    SaveHistoricalParams,
    SaveResult,
)


@final
class SQLitePriceRepository(PriceRepository):
    """SQLite adapter for price repository."""

    def _connect_for_bars(self, symbol: str):
        """Create a database connection to an SQLite database"""
        path = f"{SqlLiteConfig.SQLITE_PATH}/{self.broker.value}"
        filename = f"{symbol}.db"
        os.makedirs(path, exist_ok=True)
        return sqlite3.connect(f"{path}/{filename}")

    def _connect_for_assets(self):
        """create a database connection to an SQLite database"""
        path = f"{SqlLiteConfig.SQLITE_PATH}"
        filename = "assets.db"
        os.makedirs(path, exist_ok=True)
        return sqlite3.connect(f"{path}/{filename}")

    def save_assets(self, assets: AssetDataFrame) -> SaveResult:
        """Save assets data."""
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

    def save_historical(self, params: SaveHistoricalParams) -> SaveResult:
        """Save historical price data."""
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

    def load_assets(self) -> AssetDataFrame:
        con = self._connect_for_assets()
        try:
            query = f"SELECT * FROM {self.broker.value}"
            df = pd.read_sql(query, con=con)  # type: ignore
            # Transform to boolean because it is stored as integer in SQLite.
            df["tradable"] = df["tradable"].astype(bool)
            return AssetDataFrame(df)
        finally:
            con.close()

    def load_historical(self, params: LoadHistoricalParams) -> BarDataFrame:
        con = self._connect_for_bars(symbol=params.symbol)
        try:
            table = f"tf_{params.timeframe.name_value}"

            query = f"SELECT * FROM {table}"
            if params.start is not None:
                query += f" WHERE timestamp >= '{params.start}'"
            if params.end is not None:
                query += f" AND timestamp <= '{params.end}'"

            # Always order by timestamp to ensure give the most recent data.
            query += " ORDER BY timestamp DESC"

            if params.limit is not None:
                query += f" LIMIT {params.limit}"

            df = pd.read_sql(query, con)  # type: ignore
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)  # type: ignore

            return BarDataFrame(df)
        finally:
            con.close()
