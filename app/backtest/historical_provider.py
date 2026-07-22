"""
Historical data provider abstraction for Project Falcon.

Defines the interface implemented by all historical market
data sources used during backtesting.

Responsibilities:
    - Provide historical market candles.
    - Hide the underlying storage implementation.
    - Supply candles in chronological order.

The HistoricalDataProvider intentionally does NOT implement:

    - CSV parsing
    - Database access
    - Network downloads
    - Replay logic
    - Strategy execution
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable


class HistoricalDataProvider(ABC):
    """
    Abstract interface for historical market data providers.

    Concrete implementations may load historical data from:

        - CSV files
        - SQLite
        - Parquet
        - Remote APIs
        - Memory

    The replay engine depends only on this abstraction.
    """

    @abstractmethod
    def candles(self) -> Iterable:
        """
        Return an iterable of historical candles.

        Returns
        -------
        Iterable
            Historical candle sequence ordered
            from oldest to newest.
        """
        raise NotImplementedError