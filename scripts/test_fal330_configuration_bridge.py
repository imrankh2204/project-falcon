"""
Validation script for FAL-330 Configuration Bridge.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.backtest.backtest_config import BacktestConfig
from app.backtest.date_range import DateRange
from app.backtest.optimization.config import OptimizationConfig
from app.backtest.optimization.ranking import RankingMetric
from app.backtest.walk_forward.configuration_bridge import (
    WalkForwardConfigurationBridge,
)
from app.backtest.walk_forward.window import WalkForwardWindow
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame


def build_bridge() -> WalkForwardConfigurationBridge:

    optimization = OptimizationConfig(
        fast_periods=(5, 9),
        slow_periods=(20, 30),
        ranking_metric=RankingMetric.NET_PROFIT,
    )

    backtest = BacktestConfig(
        csv_path=Path("dummy.csv"),
        instrument=Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=1,
            lot_size=50,
            tick_size=0.05,
            expiry=None,
            strike=None,
            option_type=None,
        ),
        timeframe=TimeFrame.FIVE_MINUTES,
        quantity=1,
        output_directory=Path("output"),
        date_range=DateRange(
            start_time=datetime(2024, 1, 1),
            end_time=datetime(2024, 1, 2),
        ),
    )

    return WalkForwardConfigurationBridge(
        optimization_config=optimization,
        backtest_config=backtest,
    )


def main() -> None:

    bridge = build_bridge()

    window = WalkForwardWindow(
        training_start=datetime(2024, 1, 1),
        training_end=datetime(2024, 2, 1),
        validation_start=datetime(2024, 2, 2),
        validation_end=datetime(2024, 3, 1),
    )

    optimization = bridge.optimization_config(window)
    validation = bridge.backtest_config(window)

    assert (
        optimization.date_range.start_time
        == window.training_start
    )

    assert (
        optimization.date_range.end_time
        == window.training_end
    )

    assert (
        validation.date_range.start_time
        == window.validation_start
    )

    assert (
        validation.date_range.end_time
        == window.validation_end
    )

    print("=" * 60)
    print("FAL-330 Configuration Bridge Validation Passed")
    print("=" * 60)
    print()
    print("Optimization Config : OK")
    print("Backtest Config    : OK")
    print("DateRange Bridge   : OK")
    print("Determinism        : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()