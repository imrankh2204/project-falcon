"""
CSV Historical Provider validation tests.

This module validates the production behavior of
``CsvHistoricalProvider`` including:

- CSV loading
- Candle construction
- chronological ordering
- timeframe propagation
- cached iteration
- fail-fast validation

The tests intentionally use temporary runtime CSV fixtures to avoid
repository-level test data dependencies.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from app.backtest.csv_provider import CsvHistoricalProvider
from app.market.timeframe import TimeFrame


def _write_csv(
    directory: Path,
    content: str,
) -> Path:
    """
    Create a temporary CSV fixture.

    Parameters
    ----------
    directory:
        Temporary directory location.

    content:
        CSV file content.

    Returns
    -------
    Path
        Created CSV file path.
    """

    csv_path = directory / "historical_data.csv"

    csv_path.write_text(
        content,
        encoding="utf-8",
    )

    return csv_path


def _valid_csv() -> str:
    """
    Return a valid historical candle CSV fixture.

    Returns
    -------
    str
        CSV content.
    """

    return (
        "timestamp,open,high,low,close,volume\n"
        "2026-01-01 09:16:00,100,105,99,103,1200\n"
        "2026-01-01 09:15:00,95,101,94,100,1500\n"
        "2026-01-01 09:17:00,103,106,102,105,1300\n"
    )


def test_csv_provider_loads_valid_csv() -> None:
    """
    Validate successful CSV loading.

    Ensures:
    - provider construction succeeds
    - candle count matches source rows
    - candle objects are created
    """

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            _valid_csv(),
        )

        provider = CsvHistoricalProvider(
            csv_path,
            TimeFrame.ONE_MINUTE,
        )

        candles = list(provider.candles())

        assert len(candles) == 3


def test_csv_provider_sorts_candles_chronologically() -> None:
    """
    Validate chronological ordering.

    CSV input intentionally contains timestamps out of order.
    Provider must return sorted candle sequence.
    """

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            _valid_csv(),
        )

        provider = CsvHistoricalProvider(
            csv_path,
            TimeFrame.ONE_MINUTE,
        )

        candles = list(provider.candles())

        timestamps = [
            candle.timestamp
            for candle in candles
        ]

        assert timestamps == sorted(timestamps)


def test_csv_provider_assigns_requested_timeframe() -> None:
    """
    Validate timeframe propagation into Candle objects.
    """

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            _valid_csv(),
        )

        provider = CsvHistoricalProvider(
            csv_path,
            TimeFrame.FIVE_MINUTES,
        )

        candles = list(provider.candles())

        assert all(
            candle.timeframe == TimeFrame.FIVE_MINUTES
            for candle in candles
        )


def test_csv_provider_parses_ohlcv_values() -> None:
    """
    Validate OHLCV field conversion.
    """

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            _valid_csv(),
        )

        provider = CsvHistoricalProvider(
            csv_path,
            TimeFrame.ONE_MINUTE,
        )

        candles = list(provider.candles())

        first = candles[0]

        assert first.open == 95.0
        assert first.high == 101.0
        assert first.low == 94.0
        assert first.close == 100.0
        assert first.volume == 1500.0


def test_csv_provider_returns_independent_iterators() -> None:
    """
    Validate cached candle iteration behavior.

    Multiple calls to ``candles()`` must return independent
    iterators over the immutable cached dataset.
    """

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            _valid_csv(),
        )

        provider = CsvHistoricalProvider(
            csv_path,
            TimeFrame.ONE_MINUTE,
        )

        first_iteration = list(provider.candles())
        second_iteration = list(provider.candles())

        assert first_iteration == second_iteration
        assert first_iteration is not second_iteration


def test_csv_provider_rejects_missing_file() -> None:
    """
    Validate missing CSV file failure.
    """

    with tempfile.TemporaryDirectory() as temp:
        missing_path = (
            Path(temp)
            / "missing.csv"
        )

        try:
            CsvHistoricalProvider(
                missing_path,
                TimeFrame.ONE_MINUTE,
            )
        except FileNotFoundError:
            return

        raise AssertionError(
            "Expected FileNotFoundError for missing CSV file."
        )


def test_csv_provider_rejects_directory_path() -> None:
    """
    Validate rejection of directory paths.
    """

    with tempfile.TemporaryDirectory() as temp:
        directory = Path(temp)

        try:
            CsvHistoricalProvider(
                directory,
                TimeFrame.ONE_MINUTE,
            )
        except ValueError:
            return

        raise AssertionError(
            "Expected ValueError for directory CSV path."
        )


def test_csv_provider_rejects_missing_header_row() -> None:
    """
    Validate missing CSV header detection.
    """

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            "",
        )

        try:
            CsvHistoricalProvider(
                csv_path,
                TimeFrame.ONE_MINUTE,
            )
        except ValueError:
            return

        raise AssertionError(
            "Expected ValueError for missing header row."
        )


def test_csv_provider_rejects_missing_columns() -> None:
    """
    Validate required column enforcement.
    """

    csv_content = (
        "timestamp,open,high,low,close\n"
        "2026-01-01 09:15:00,"
        "100,105,99,103\n"
    )

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            csv_content,
        )

        try:
            CsvHistoricalProvider(
                csv_path,
                TimeFrame.ONE_MINUTE,
            )
        except ValueError:
            return

        raise AssertionError(
            "Expected ValueError for missing required columns."
        )


def test_csv_provider_rejects_invalid_timestamp() -> None:
    """
    Validate timestamp format enforcement.
    """

    csv_content = (
        "timestamp,open,high,low,close,volume\n"
        "2026-01-01,100,105,99,103,1200\n"
    )

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            csv_content,
        )

        try:
            CsvHistoricalProvider(
                csv_path,
                TimeFrame.ONE_MINUTE,
            )
        except ValueError:
            return

        raise AssertionError(
            "Expected ValueError for invalid timestamp."
        )


def test_csv_provider_rejects_invalid_numeric_value() -> None:
    """
    Validate numeric conversion failure.
    """

    csv_content = (
        "timestamp,open,high,low,close,volume\n"
        "2026-01-01 09:15:00,"
        "invalid,105,99,103,1200\n"
    )

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            csv_content,
        )

        try:
            CsvHistoricalProvider(
                csv_path,
                TimeFrame.ONE_MINUTE,
            )
        except ValueError:
            return

        raise AssertionError(
            "Expected ValueError for invalid numeric data."
        )

def test_csv_provider_rejects_invalid_price_relationship() -> None:
    """
    Validate OHLC consistency checks.

    Provider must reject candles where high price
    is lower than low price.
    """

    csv_content = (
        "timestamp,open,high,low,close,volume\n"
        "2026-01-01 09:15:00,"
        "100,90,95,103,1200\n"
    )

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            csv_content,
        )

        try:
            CsvHistoricalProvider(
                csv_path,
                TimeFrame.ONE_MINUTE,
            )
        except ValueError:
            return

        raise AssertionError(
            "Expected ValueError for invalid high/low relationship."
        )


def test_csv_provider_rejects_empty_required_field() -> None:
    """
    Validate required field emptiness detection.
    """

    csv_content = (
        "timestamp,open,high,low,close,volume\n"
        "2026-01-01 09:15:00,"
        ",105,99,103,1200\n"
    )

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            csv_content,
        )

        try:
            CsvHistoricalProvider(
                csv_path,
                TimeFrame.ONE_MINUTE,
            )
        except ValueError:
            return

        raise AssertionError(
            "Expected ValueError for empty required field."
        )


def test_csv_provider_rejects_invalid_csv_path_type() -> None:
    """
    Validate constructor type checking for CSV path.
    """

    try:
        CsvHistoricalProvider(
            123,  # type: ignore[arg-type]
            TimeFrame.ONE_MINUTE,
        )
    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError for invalid csv_path type."
    )


def test_csv_provider_rejects_invalid_timeframe_type() -> None:
    """
    Validate constructor type checking for timeframe.
    """

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            _valid_csv(),
        )

        try:
            CsvHistoricalProvider(
                csv_path,
                "1m",  # type: ignore[arg-type]
            )
        except TypeError:
            return

        raise AssertionError(
            "Expected TypeError for invalid timeframe type."
        )


def test_csv_provider_empty_dataset_is_supported() -> None:
    """
    Validate provider behavior with a valid header-only CSV.

    A header-only historical source should produce an empty
    immutable candle cache.
    """

    csv_content = (
        "timestamp,open,high,low,close,volume\n"
    )

    with tempfile.TemporaryDirectory() as temp:
        csv_path = _write_csv(
            Path(temp),
            csv_content,
        )

        provider = CsvHistoricalProvider(
            csv_path,
            TimeFrame.ONE_MINUTE,
        )

        assert list(provider.candles()) == []


def run_tests() -> None:
    """
    Execute all CSV provider validation tests.

    This lightweight runner keeps the script executable without
    introducing an external test framework dependency.
    """

    tests = [
        test_csv_provider_loads_valid_csv,
        test_csv_provider_sorts_candles_chronologically,
        test_csv_provider_assigns_requested_timeframe,
        test_csv_provider_parses_ohlcv_values,
        test_csv_provider_returns_independent_iterators,
        test_csv_provider_rejects_missing_file,
        test_csv_provider_rejects_directory_path,
        test_csv_provider_rejects_missing_header_row,
        test_csv_provider_rejects_missing_columns,
        test_csv_provider_rejects_invalid_timestamp,
        test_csv_provider_rejects_invalid_numeric_value,
        test_csv_provider_rejects_invalid_price_relationship,
        test_csv_provider_rejects_empty_required_field,
        test_csv_provider_rejects_invalid_csv_path_type,
        test_csv_provider_rejects_invalid_timeframe_type,
        test_csv_provider_empty_dataset_is_supported,
    ]

    for test in tests:
        test()
        print(f"PASSED: {test.__name__}")


if __name__ == "__main__":
    run_tests()