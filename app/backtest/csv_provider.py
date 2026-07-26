"""
CSV-backed historical data provider.

This module provides a production-ready implementation of
``HistoricalDataProvider`` that loads historical OHLCV candle data from a CSV
file, validates it during construction, converts every record into the
project's ``Candle`` domain model, optionally filters candles using a
``DateRange``, and caches the resulting objects for subsequent iteration.

Design principles:
- Fail-fast validation
- Immutable cached historical dataset
- Deterministic date filtering
- Single responsibility
- Strong typing
- No replay or execution responsibilities
"""

from __future__ import annotations

import csv
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Final

from app.backtest.date_range import (
    DateRange,
)
from app.backtest.historical_provider import (
    HistoricalDataProvider,
)
from app.market.candle import Candle
from app.market.timeframe import TimeFrame


class CsvHistoricalProvider(HistoricalDataProvider):
    """
    Historical data provider backed by a CSV file.

    The CSV file is fully validated and loaded during initialization.
    After construction, candle iteration is performed from an in-memory cache,
    avoiding repeated file I/O.

    Optional DateRange filtering is applied during loading so the cached
    dataset always represents the configured execution window.

    Required CSV columns::

        timestamp
        open
        high
        low
        close
        volume

    Timestamp format::

        YYYY-MM-DD HH:MM:SS

    Parameters
    ----------
    csv_path:
        Path to the CSV file.

    timeframe:
        Timeframe assigned to every constructed Candle.

    date_range:
        Optional inclusive execution time window.

    Raises
    ------
    TypeError
        If constructor arguments have invalid types.

    FileNotFoundError
        If the CSV file does not exist.

    ValueError
        If the CSV is malformed or contains invalid data.
    """

    _TIMESTAMP_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

    _REQUIRED_COLUMNS: Final[frozenset[str]] = frozenset(
        {
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
        }
    )

    def __init__(
        self,
        csv_path: str | Path,
        timeframe: TimeFrame,
        date_range: DateRange | None = None,
    ) -> None:

        if not isinstance(
            csv_path,
            (str, Path),
        ):
            raise TypeError(
                "csv_path must be of type str or pathlib.Path."
            )

        if not isinstance(
            timeframe,
            TimeFrame,
        ):
            raise TypeError(
                "timeframe must be an instance of TimeFrame."
            )

        if (
            date_range is not None
            and not isinstance(
                date_range,
                DateRange,
            )
        ):
            raise TypeError(
                "date_range must be a DateRange or None."
            )

        self._path: Path = Path(csv_path)
        self._timeframe: TimeFrame = timeframe
        self._date_range = date_range

        if not self._path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {self._path}"
            )

        if not self._path.is_file():
            raise ValueError(
                f"CSV path is not a file: {self._path}"
            )

        self._candles: tuple[Candle, ...] = self._load()

    def candles(self) -> Iterator[Candle]:
        """
        Return an iterator over cached historical candles.

        Returns
        -------
        Iterator[Candle]
            Chronologically sorted candle sequence.
        """

        return iter(self._candles)

    def _load(self) -> tuple[Candle, ...]:
        """
        Load, validate, filter, and cache candles from CSV.

        Returns
        -------
        tuple[Candle, ...]
            Chronologically sorted candle cache.
        """

        candles: list[Candle] = []

        with self._path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            if reader.fieldnames is None:
                raise ValueError(
                    "CSV file is missing a header row."
                )

            fieldnames = {
                field.strip()
                for field in reader.fieldnames
                if field is not None
            }

            missing = self._REQUIRED_COLUMNS - fieldnames

            if missing:
                raise ValueError(
                    "CSV missing required columns: "
                    + ", ".join(sorted(missing))
                )

            for line_number, row in enumerate(
                reader,
                start=2,
            ):

                candle = self._build_candle(
                    row=row,
                    line_number=line_number,
                )

                if self._within_date_range(candle):
                    candles.append(candle)

        candles.sort(
            key=lambda candle: candle.timestamp
        )

        return tuple(candles)

    def _within_date_range(
        self,
        candle: Candle,
    ) -> bool:
        """
        Determine whether a candle belongs to the configured date range.

        DateRange boundaries are inclusive.

        Returns
        -------
        bool
            True if candle is within execution window.
        """

        if self._date_range is None:
            return True
        
        return (
            self._date_range.start_time
            <= candle.timestamp
            <= self._date_range.end_time
        )

    def _build_candle(
        self,
        *,
        row: dict[str, str | None],
        line_number: int,
    ) -> Candle:
        """
        Construct a validated Candle from CSV row.
        """

        try:
            timestamp_text = self._require(
                row,
                "timestamp",
            )

            open_text = self._require(
                row,
                "open",
            )

            high_text = self._require(
                row,
                "high",
            )

            low_text = self._require(
                row,
                "low",
            )

            close_text = self._require(
                row,
                "close",
            )

            volume_text = self._require(
                row,
                "volume",
            )

            timestamp = datetime.strptime(
                timestamp_text,
                self._TIMESTAMP_FORMAT,
            )

            open_price = float(open_text)
            high_price = float(high_text)
            low_price = float(low_text)
            close_price = float(close_text)
            volume = float(volume_text)

        except ValueError as exc:
            raise ValueError(
                f"Invalid data at CSV line {line_number}: {exc}"
            ) from exc

        if high_price < low_price:
            raise ValueError(
                f"Invalid data at CSV line {line_number}: "
                "high is less than low."
            )

        return Candle(
            timestamp=timestamp,
            timeframe=self._timeframe,
            open=open_price,
            high=high_price,
            low=low_price,
            close=close_price,
            volume=volume,
        )

    @staticmethod
    def _require(
        row: dict[str, str | None],
        column: str,
    ) -> str:
        """
        Retrieve and validate a required CSV field.
        """

        value = row.get(column)

        if value is None:
            raise ValueError(
                f"Missing value for '{column}'."
            )

        value = value.strip()

        if not value:
            raise ValueError(
                f"Empty value for '{column}'."
            )

        return value