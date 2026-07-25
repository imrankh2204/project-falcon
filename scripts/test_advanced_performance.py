"""
Standalone validation for FAL-230-R1.

Validates:
    - Profit Factor
    - Expectancy
    - Sharpe Ratio
    - Sortino Ratio
    - Edge cases
    - Deterministic calculations
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.backtest.advanced_metrics import (
    AdvancedPerformanceMetrics,
)
from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.position import Position
from app.trading.position_status import PositionStatus


def create_position(
    *,
    pnl: float,
    index: int,
) -> Position:
    """
    Create a closed position with deterministic P&L.
    """

    instrument = Instrument(
        exchange="NSE",
        symbol="NIFTY",
        instrument_token=0,
        lot_size=50,
        tick_size=0.05,
    )

    entry_time = (
        datetime(2026, 1, 1, 9, 15)
        +
        timedelta(minutes=index)
    )

    position = Position(
        position_id=f"TEST-{index}",
        instrument=instrument,
        signal=Signal.BUY,
        quantity=1,
        entry_price=100.0,
        entry_time=entry_time,
    )

    exit_price = (
        position.entry_price
        +
        pnl
    )

    position.close(
        exit_price=exit_price,
        exit_time=entry_time + timedelta(minutes=5),
    )

    return position


def test_profit_factor() -> None:
    positions = [
        create_position(
            pnl=100,
            index=1,
        ),
        create_position(
            pnl=-50,
            index=2,
        ),
    ]

    snapshot = (
        AdvancedPerformanceMetrics.calculate(
            positions
        )
    )

    assert (
        snapshot.profit_factor
        ==
        2.0
    )


def test_expectancy() -> None:
    positions = [
        create_position(
            pnl=100,
            index=1,
        ),
        create_position(
            pnl=-50,
            index=2,
        ),
    ]

    snapshot = (
        AdvancedPerformanceMetrics.calculate(
            positions
        )
    )

    assert (
        snapshot.expectancy
        ==
        25.0
    )


def test_sharpe_ratio() -> None:
    positions = [
        create_position(
            pnl=100,
            index=1,
        ),
        create_position(
            pnl=-50,
            index=2,
        ),
        create_position(
            pnl=50,
            index=3,
        ),
    ]

    snapshot = (
        AdvancedPerformanceMetrics.calculate(
            positions
        )
    )

    assert snapshot.sharpe_ratio != 0.0


def test_sortino_ratio() -> None:
    positions = [
        create_position(
            pnl=100,
            index=1,
        ),
        create_position(
            pnl=-50,
            index=2,
        ),
        create_position(
            pnl=-25,
            index=3,
        ),
        create_position(
            pnl=75,
            index=4,
        ),
    ]

    snapshot = (
        AdvancedPerformanceMetrics.calculate(
            positions
        )
    )

    assert snapshot.sortino_ratio != 0.0


def test_empty_dataset() -> None:
    snapshot = (
        AdvancedPerformanceMetrics.calculate(
            []
        )
    )

    assert snapshot.profit_factor == 0.0
    assert snapshot.expectancy == 0.0
    assert snapshot.sharpe_ratio == 0.0
    assert snapshot.sortino_ratio == 0.0


def test_open_position_rejected() -> None:
    instrument = Instrument(
        exchange="NSE",
        symbol="NIFTY",
        instrument_token=0,
        lot_size=50,
        tick_size=0.05,
    )

    position = Position(
        position_id="OPEN-1",
        instrument=instrument,
        signal=Signal.BUY,
        quantity=1,
        entry_price=100.0,
        entry_time=datetime(2026, 1, 1, 9, 15),
        status=PositionStatus.OPEN,
    )

    try:
        AdvancedPerformanceMetrics.calculate(
            [position]
        )

    except ValueError:
        return

    raise AssertionError(
        "Open positions must be rejected."
    )


def test_determinism() -> None:
    positions = [
        create_position(
            pnl=100,
            index=1,
        ),
        create_position(
            pnl=-50,
            index=2,
        ),
    ]

    first = (
        AdvancedPerformanceMetrics.calculate(
            positions
        )
    )

    second = (
        AdvancedPerformanceMetrics.calculate(
            positions
        )
    )

    assert first == second


def main() -> None:

    test_profit_factor()
    test_expectancy()
    test_sharpe_ratio()
    test_sortino_ratio()
    test_empty_dataset()
    test_open_position_rejected()
    test_determinism()

    print("=" * 60)
    print(
        "Advanced Performance Analytics Validation Passed"
    )
    print("=" * 60)
    print()
    print("Profit Factor     : OK")
    print("Expectancy        : OK")
    print("Sharpe Ratio      : OK")
    print("Sortino Ratio     : OK")
    print("Edge Cases        : OK")
    print("Determinism       : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()