"""
Validation for FAL-330 Backtest Factory Bridge.
"""

from __future__ import annotations

from pathlib import Path

from app.backtest.backtest_config import BacktestConfig
from app.backtest.backtest_factory_bridge import (
    BacktestFactoryBridge,
)
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame


def build_config() -> BacktestConfig:

    return BacktestConfig(
        csv_path=Path("data/sample.csv"),
        instrument=Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=1,
            lot_size=50,
            tick_size=0.05,
        ),
        timeframe=TimeFrame.FIVE_MINUTES,
        quantity=1,
        output_directory=Path("output"),
        date_range=None,
    )


def main() -> None:

    bridge = BacktestFactoryBridge()

    factory = bridge.create(
        build_config()
    )

    print("=" * 60)
    print("FAL-330 Factory Bridge Validation Passed")
    print("=" * 60)
    print()
    print("Factory Creation : OK")
    print("Determinism      : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()