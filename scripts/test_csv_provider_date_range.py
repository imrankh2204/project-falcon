"""
CSV Historical Provider DateRange validation for Project Falcon.

Validates:
- Full dataset loading.
- DateRange filtering.
- Inclusive boundaries.
- Deterministic candle ordering.
- Invalid date range type rejection.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from app.backtest.csv_provider import (
    CsvHistoricalProvider,
)
from app.backtest.date_range import (
    DateRange,
)
from app.market.timeframe import (
    TimeFrame,
)


CSV_CONTENT = """timestamp,open,high,low,close,volume
2026-01-01 09:15:00,100,105,99,103,1000
2026-01-01 09:20:00,103,108,102,107,1200
2026-01-01 09:25:00,107,110,106,109,1500
2026-01-01 09:30:00,109,112,108,111,1300
"""


def create_csv() -> Path:
    """
    Create temporary historical CSV dataset.
    """

    directory = TemporaryDirectory()

    path = Path(
        directory.name
    ) / "historical.csv"

    path.write_text(
        CSV_CONTENT,
        encoding="utf-8",
    )

    return path


def test_full_loading(
    csv_path: Path,
) -> None:

    provider = CsvHistoricalProvider(
        csv_path=csv_path,
        timeframe=TimeFrame.FIVE_MINUTES,
    )

    candles = tuple(
        provider.candles()
    )

    assert len(candles) == 4


def test_date_range_filtering(
    csv_path: Path,
) -> None:

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

    provider = CsvHistoricalProvider(
        csv_path=csv_path,
        timeframe=TimeFrame.FIVE_MINUTES,
        date_range=date_range,
    )

    candles = tuple(
        provider.candles()
    )

    assert len(candles) == 3

    assert (
        candles[0].timestamp
        ==
        datetime.strptime(
            "2026-01-01 09:20:00",
            "%Y-%m-%d %H:%M:%S",
        )
    )

    assert (
        candles[-1].timestamp
        ==
        datetime.strptime(
            "2026-01-01 09:30:00",
            "%Y-%m-%d %H:%M:%S",
        )
    )


def test_determinism(
    csv_path: Path,
) -> None:

    date_range = DateRange(
        start_time=datetime.strptime(
            "2026-01-01 09:15:00",
            "%Y-%m-%d %H:%M:%S",
        ),
        end_time=datetime.strptime(
            "2026-01-01 09:25:00",
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


def test_invalid_date_range_type(
    csv_path: Path,
) -> None:

    try:
        CsvHistoricalProvider(
            csv_path=csv_path,
            timeframe=TimeFrame.FIVE_MINUTES,
            date_range="invalid",
        )

    except TypeError:
        return

    raise AssertionError(
        "Invalid date_range type was accepted."
    )


def main() -> None:

    with TemporaryDirectory() as directory:

        csv_path = Path(directory) / "historical.csv"

        csv_path.write_text(
            CSV_CONTENT,
            encoding="utf-8",
        )

        test_full_loading(
            csv_path
        )

        test_date_range_filtering(
            csv_path
        )

        test_determinism(
            csv_path
        )

        test_invalid_date_range_type(
            csv_path
        )

    print("=" * 60)
    print(
        "CSV Provider DateRange Validation Passed"
    )
    print("=" * 60)
    print()
    print(
        "Loading          : OK"
    )
    print(
        "Filtering        : OK"
    )
    print(
        "Boundary         : OK"
    )
    print(
        "Determinism      : OK"
    )
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()