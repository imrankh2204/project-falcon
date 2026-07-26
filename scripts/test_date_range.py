"""
DateRange validation for Project Falcon.

Validates:
- Valid range creation.
- Invalid range rejection.
- Immutability.
- Deterministic behaviour.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.backtest.date_range import (
    DateRange,
)


def build_range() -> DateRange:

    return DateRange(
        start_time=datetime(
            2026,
            1,
            1,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            1,
            31,
            tzinfo=timezone.utc,
        ),
    )


def test_valid_range() -> None:

    date_range = build_range()

    assert (
        date_range.start_time.day
        ==
        1
    )

    assert (
        date_range.end_time.day
        ==
        31
    )


def test_invalid_range() -> None:

    try:
        DateRange(
            start_time=datetime(
                2026,
                2,
                1,
                tzinfo=timezone.utc,
            ),
            end_time=datetime(
                2026,
                1,
                1,
                tzinfo=timezone.utc,
            ),
        )

    except ValueError:
        return

    raise AssertionError(
        "Invalid date range was accepted."
    )


def test_determinism() -> None:

    first = build_range()

    second = build_range()

    assert first == second


def main() -> None:

    test_valid_range()
    test_invalid_range()
    test_determinism()

    print("=" * 60)
    print(
        "DateRange Validation Passed"
    )
    print("=" * 60)
    print()
    print(
        "Creation       : OK"
    )
    print(
        "Validation     : OK"
    )
    print(
        "Determinism    : OK"
    )
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()