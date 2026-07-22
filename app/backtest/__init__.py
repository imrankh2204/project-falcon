"""
Backtesting framework for Project Falcon.

This package contains the infrastructure required to replay
historical market data through the existing trading domain.

Modules
-------
historical_provider
    Abstract interface for historical market data sources.

csv_provider
    CSV-based implementation of HistoricalDataProvider.

replay_clock
    Deterministic clock used during historical replay.

replay_engine
    Coordinates replay components while remaining independent
    from strategy and broker implementations.
"""

from __future__ import annotations

from app.backtest.csv_provider import CsvHistoricalProvider
from app.backtest.historical_provider import HistoricalDataProvider
from app.backtest.replay_clock import ReplayClock
from app.backtest.replay_engine import ReplayEngine

__all__ = [
    "HistoricalDataProvider",
    "CsvHistoricalProvider",
    "ReplayClock",
    "ReplayEngine",
]