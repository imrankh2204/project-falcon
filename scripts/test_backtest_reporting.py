"""
Reporting validation for Project Falcon.

Validates the reporting subsystem independently from replay,
strategy execution, and application orchestration.

Responsibilities
----------------
- Validate ReportBuilder.
- Validate ConsoleExporter.
- Validate CsvExporter.
- Validate JsonExporter.

This validation intentionally does NOT execute:

- ReplayEngine
- BacktestSession
- BacktestApplication
- TradingService
- Strategy evaluation
"""

from __future__ import annotations

import csv
import json
from datetime import datetime

from app.backtest.backtest_result import BacktestResult
from app.backtest.performance_snapshot import PerformanceSnapshot
from app.backtest.reporting.builder import ReportBuilder
from app.backtest.reporting.console import ConsoleExporter
from app.backtest.reporting.csv import CsvExporter
from app.backtest.reporting.json import JsonExporter
from app.market.instrument import Instrument


def build_result() -> BacktestResult:
    """
    Construct a deterministic BacktestResult for validation.
    """

    performance = PerformanceSnapshot(
        trade_count=10,
        winning_trades=6,
        losing_trades=4,
        win_rate=60.0,
        gross_profit=1250.50,
        gross_loss=-430.25,
        net_profit=820.25,
        average_win=208.42,
        average_loss=-107.56,
        largest_win=450.00,
        largest_loss=-180.00,
    )

    return BacktestResult(
        instrument=Instrument(
            exchange="NSE",
            symbol="NIFTY",
            instrument_token=12345,
            lot_size=50,
            tick_size=0.05,
        ),
        strategy_name="EMACrossoverStrategy",
        start_time=datetime(2026, 1, 1, 9, 15),
        end_time=datetime(2026, 1, 1, 15, 30),
        performance=performance,
    )


def validate_report_builder(result: BacktestResult) -> None:
    """
    Validate ReportBuilder.
    """

    report = ReportBuilder().build(result)

    assert report.instrument == result.instrument
    assert report.strategy_name == result.strategy_name
    assert report.start_time == result.start_time
    assert report.end_time == result.end_time
    assert report.performance == result.performance


def validate_console_export(result: BacktestResult) -> None:
    """
    Validate ConsoleExporter.
    """

    report = ReportBuilder().build(result)

    text = ConsoleExporter().export(report)

    assert "EMACrossoverStrategy" in text
    assert "NIFTY" in text
    assert "Trade Count" in text
    assert "10" in text
    assert "60.00%" in text
    assert "1250.50" in text
    assert "-430.25" in text
    assert "820.25" in text


def validate_csv_export(result: BacktestResult) -> None:
    """
    Validate CsvExporter.
    """

    report = ReportBuilder().build(result)

    text = CsvExporter().export(report)

    rows = list(csv.reader(text.splitlines()))

    assert len(rows) == 2

    header = rows[0]
    values = rows[1]

    assert header[0] == "strategy_name"
    assert values[0] == "EMACrossoverStrategy"
    assert values[1] == "NIFTY"
    assert values[4] == "10"


def validate_json_export(result: BacktestResult) -> None:
    """
    Validate JsonExporter.
    """

    report = ReportBuilder().build(result)

    payload = json.loads(
        JsonExporter().export(report)
    )

    assert payload["strategy_name"] == "EMACrossoverStrategy"

    assert payload["instrument"]["symbol"] == "NIFTY"

    assert payload["performance"]["trade_count"] == 10

    assert payload["performance"]["winning_trades"] == 6

    assert payload["performance"]["net_profit"] == 820.25

    assert payload["start_time"] == "2026-01-01T09:15:00"

    assert payload["end_time"] == "2026-01-01T15:30:00"


def main() -> None:
    """
    Execute reporting validation.
    """

    result = build_result()

    validate_report_builder(result)
    validate_console_export(result)
    validate_csv_export(result)
    validate_json_export(result)

    print("=" * 60)
    print("Backtest Reporting Validation Passed")
    print("=" * 60)
    print()

    print("Report Builder     : OK")
    print("Console Exporter   : OK")
    print("CSV Exporter       : OK")
    print("JSON Exporter      : OK")
    print()

    print("=" * 60)


if __name__ == "__main__":
    main()