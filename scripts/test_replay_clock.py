"""
ReplayClock validation tests.

This module validates the deterministic replay clock behavior
used by Project Falcon historical replay.

Validation coverage:

- Initialization
- Current simulated time access
- Forward advancement
- Equal timestamp handling
- Backward movement protection
- Fail-fast type validation

The tests intentionally avoid external frameworks to keep the
validation layer lightweight and deterministic.
"""

from __future__ import annotations

from datetime import datetime

from app.backtest.replay_clock import ReplayClock


def test_replay_clock_initializes_with_valid_datetime() -> None:
    """
    Validate successful clock initialization.
    """

    start_time = datetime(
        2026,
        1,
        1,
        9,
        15,
    )

    clock = ReplayClock(start_time)

    assert clock.current_time == start_time


def test_replay_clock_exposes_current_time() -> None:
    """
    Validate current_time property behavior.
    """

    start_time = datetime(
        2026,
        1,
        1,
        9,
        15,
    )

    clock = ReplayClock(start_time)

    current = clock.current_time

    assert current == start_time


def test_replay_clock_advances_forward() -> None:
    """
    Validate chronological forward movement.
    """

    start_time = datetime(
        2026,
        1,
        1,
        9,
        15,
    )

    next_time = datetime(
        2026,
        1,
        1,
        9,
        16,
    )

    clock = ReplayClock(start_time)

    clock.advance(next_time)

    assert clock.current_time == next_time


def test_replay_clock_allows_equal_timestamp() -> None:
    """
    Validate same timestamp advancement.

    Replay systems may encounter multiple events
    at identical timestamps.
    """

    timestamp = datetime(
        2026,
        1,
        1,
        9,
        15,
    )

    clock = ReplayClock(timestamp)

    clock.advance(timestamp)

    assert clock.current_time == timestamp


def test_replay_clock_rejects_backward_time() -> None:
    """
    Validate prevention of backward movement.
    """

    start_time = datetime(
        2026,
        1,
        1,
        9,
        15,
    )

    earlier_time = datetime(
        2026,
        1,
        1,
        9,
        14,
    )

    clock = ReplayClock(start_time)

    try:
        clock.advance(earlier_time)

    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for backward time movement."
    )


def test_replay_clock_rejects_invalid_start_time_type() -> None:
    """
    Validate constructor type checking.
    """

    try:
        ReplayClock(
            "2026-01-01 09:15:00",  # type: ignore[arg-type]
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError for invalid start_time type."
    )


def test_replay_clock_rejects_invalid_advance_time_type() -> None:
    """
    Validate advance() type checking.
    """

    start_time = datetime(
        2026,
        1,
        1,
        9,
        15,
    )

    clock = ReplayClock(start_time)

    try:
        clock.advance(
            "2026-01-01 09:16:00",  # type: ignore[arg-type]
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError for invalid new_time type."
    )


def test_replay_clock_state_remains_valid_after_failed_advance() -> None:
    """
    Validate state preservation after rejected movement.

    A failed backward movement must not mutate the clock state.
    """

    start_time = datetime(
        2026,
        1,
        1,
        9,
        15,
    )

    earlier_time = datetime(
        2026,
        1,
        1,
        9,
        14,
    )

    clock = ReplayClock(start_time)

    try:
        clock.advance(earlier_time)

    except ValueError:
        pass

    else:
        raise AssertionError(
            "Expected ValueError for backward time movement."
        )

    assert clock.current_time == start_time


def run_tests() -> None:
    """
    Execute all ReplayClock validation tests.

    Provides a lightweight executable validation flow
    without requiring an external test runner.
    """

    tests = [
        test_replay_clock_initializes_with_valid_datetime,
        test_replay_clock_exposes_current_time,
        test_replay_clock_advances_forward,
        test_replay_clock_allows_equal_timestamp,
        test_replay_clock_rejects_backward_time,
        test_replay_clock_rejects_invalid_start_time_type,
        test_replay_clock_rejects_invalid_advance_time_type,
        test_replay_clock_state_remains_valid_after_failed_advance,
    ]

    for test in tests:
        test()
        print(f"PASSED: {test.__name__}")


if __name__ == "__main__":
    run_tests()