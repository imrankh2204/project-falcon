"""
Integration validation for Project Falcon BacktestApplication.

This script performs a lightweight end-to-end validation of the
backtest application by constructing the production dependency graph,
executing a backtest, and validating the returned report.

Responsibilities
----------------
- Build BacktestConfig.
- Construct BacktestApplication.
- Execute application.run().
- Validate BacktestReport.
- Print a concise validation summary.

This script intentionally does NOT implement:

- Unit testing
- Performance benchmarking
- Report exporting
- Trading logic
- Strategy logic
"""

from __future__ import annotations

from pathlib import Path

from app.backtest.backtest_config import BacktestConfig
from app.backtest.reporting.report import BacktestReport
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame
from scripts.run_backtest import build_backtest_application


def main() -> int:
    """
    Execute an integration validation of the backtest application.

    Returns
    -------
    int
        Process exit code.
    """

    config = BacktestConfig(
        csv_path=Path("data/historical/sample.csv"),
        instrument=Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=0,
            lot_size=50,
            tick_size=0.05,
        ),
        timeframe=TimeFrame.FIVE_MINUTES,
        quantity=50,
        output_directory=Path("data/reports"),
    )

    application = build_backtest_application(config)

    report = application.run()

    if not isinstance(report, BacktestReport):
        raise TypeError(
            "Application did not return a BacktestReport."
        )

    if report.instrument.symbol != "NIFTY":
        raise AssertionError(
            "Unexpected instrument."
        )

    if report.strategy_name != "EMACrossoverStrategy":
        raise AssertionError(
            "Unexpected strategy name."
        )

    if report.start_time > report.end_time:
        raise AssertionError(
            "Invalid report time range."
        )

    if report.performance.trade_count < 0:
        raise AssertionError(
            "Trade count cannot be negative."
        )

    print("=" * 60)
    print("Backtest Application Validation Passed")
    print("=" * 60)
    print()
    print(f"Strategy    : {report.strategy_name}")
    print(f"Instrument  : {report.instrument.symbol}")
    print(f"Trade Count : {report.performance.trade_count}")
    print()
    print("=" * 60)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())