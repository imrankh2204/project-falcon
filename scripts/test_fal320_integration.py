"""
FAL-320 integration validation for Project Falcon.

Validates that DateRange propagates correctly through the backtest
configuration and into the CSV historical provider while preserving
deterministic execution.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from app.backtest.backtest_config import BacktestConfig
from app.backtest.csv_provider import CsvHistoricalProvider
from app.backtest.date_range import DateRange
from app.market.instrument import Instrument
from app.market.timeframe import TimeFrame


CSV_CONTENT = """timestamp,open,high,low,close,volume
2026-01-01 09:15:00,100,105,99,103,1000
2026-01-01 09:20:00,103,108,102,107,1200
2026-01-01 09:25:00,107,110,106,109,1500
2026-01-01 09:30:00,109,112,108,111,1300
2026-01-01 09:35:00,111,114,110,113,1400
"""


def build_csv(directory: Path) -> Path:
    """
    Create a temporary historical CSV file.
    """

    csv_path = directory / "historical.csv"

    csv_path.write_text(
        CSV_CONTENT,
        encoding="utf-8",
    )

    return csv_path


def build_instrument() -> Instrument:
    """
    Construct a deterministic instrument.
    """

    return Instrument(
        exchange="NSE",
        symbol="NIFTY",
        instrument_token=1,
        lot_size=50,
        tick_size=0.05,
        expiry=None,
        strike=None,
        option_type=None,
    )


def build_config(
    csv_path: Path,
    date_range: DateRange,
) -> BacktestConfig:
    """
    Construct a BacktestConfig using a DateRange.
    """

    return BacktestConfig(
        csv_path=csv_path,
        instrument=build_instrument(),
        timeframe=TimeFrame.FIVE_MINUTES,
        quantity=1,
        output_directory=csv_path.parent,
        date_range=date_range,
    )


def test_date_range_propagation() -> None:

    with TemporaryDirectory() as temp_dir:

        directory = Path(temp_dir)

        csv_path = build_csv(directory)

        date_range = DateRange(
            start_time=datetime.strptime(
                "2026-01-01 09:20:00",
                "%Y-%m-%d %H:%M:%S",
            ),
            end_time=datetime.strptime(
                "2026-01-01 09:30:00",
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        config = build_config(
            csv_path,
            date_range,
        )

        provider = CsvHistoricalProvider(
            csv_path=config.csv_path,
            timeframe=config.timeframe,
            date_range=config.date_range,
        )

        candles = tuple(provider.candles())

        assert len(candles) == 3

        assert (
            candles[0].timestamp
            == date_range.start_time
        )

        assert (
            candles[-1].timestamp
            == date_range.end_time
        )


def test_backtest_isolation() -> None:

    with TemporaryDirectory() as temp_dir:

        directory = Path(temp_dir)

        csv_path = build_csv(directory)

        first = DateRange(
            start_time=datetime.strptime(
                "2026-01-01 09:15:00",
                "%Y-%m-%d %H:%M:%S",
            ),
            end_time=datetime.strptime(
                "2026-01-01 09:20:00",
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        second = DateRange(
            start_time=datetime.strptime(
                "2026-01-01 09:25:00",
                "%Y-%m-%d %H:%M:%S",
            ),
            end_time=datetime.strptime(
                "2026-01-01 09:35:00",
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        first_provider = CsvHistoricalProvider(
            csv_path=csv_path,
            timeframe=TimeFrame.FIVE_MINUTES,
            date_range=first,
        )

        second_provider = CsvHistoricalProvider(
            csv_path=csv_path,
            timeframe=TimeFrame.FIVE_MINUTES,
            date_range=second,
        )

        assert tuple(first_provider.candles()) != tuple(
            second_provider.candles()
        )


def test_determinism() -> None:

    with TemporaryDirectory() as temp_dir:

        directory = Path(temp_dir)

        csv_path = build_csv(directory)

        date_range = DateRange(
            start_time=datetime.strptime(
                "2026-01-01 09:20:00",
                "%Y-%m-%d %H:%M:%S",
            ),
            end_time=datetime.strptime(
                "2026-01-01 09:35:00",
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        first = tuple(
            CsvHistoricalProvider(
                csv_path=csv_path,
                timeframe=TimeFrame.FIVE_MINUTES,
                date_range=date_range,
            ).candles()
        )

        second = tuple(
            CsvHistoricalProvider(
                csv_path=csv_path,
                timeframe=TimeFrame.FIVE_MINUTES,
                date_range=date_range,
            ).candles()
        )

        assert first == second


def main() -> None:

    test_date_range_propagation()
    test_backtest_isolation()
    test_determinism()

    print("=" * 60)
    print("FAL-320 Integration Validation Passed")
    print("=" * 60)
    print()
    print("DateRange Propagation : OK")
    print("Backtest Isolation    : OK")
    print("Window Execution      : OK")
    print("Determinism           : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()