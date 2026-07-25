"""
Equity curve validation for Project Falcon.

Validates deterministic equity curve analytics.

Coverage:
    - Equity curve construction
    - Chronological equity progression
    - Drawdown calculation
    - Edge cases
    - Deterministic output
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.backtest.equity_curve import EquityCurve
from app.backtest.equity_curve_snapshot import EquityPoint
from app.strategies.signal import Signal
from app.trading.position import Position
from app.trading.position_status import PositionStatus
from app.market.instrument import Instrument


def _time(minutes: int) -> datetime:
    return datetime(
        2026,
        1,
        1,
        9,
        15,
        tzinfo=timezone.utc,
    ) + timedelta(
        minutes=minutes
    )


def _instrument() -> Instrument:
    return Instrument(
        exchange="NSE",
        symbol="NIFTY",
        instrument_token=1,
        lot_size=50,
        tick_size=0.05,
    )


def _closed_position(
    *,
    pnl: float,
    exit_minutes: int,
) -> Position:
    position = Position(
        position_id=f"POS-{exit_minutes}",
        instrument=_instrument(),
        signal=Signal.BUY,
        quantity=1,
        entry_price=100.0,
        entry_time=_time(0),
        exit_price=100.0 + pnl,
        exit_time=_time(exit_minutes),
        status=PositionStatus.OPEN,
    )

    position.close(
        exit_price=100.0 + pnl,
        exit_time=_time(exit_minutes),
    )

    return position


def test_equity_curve_construction() -> None:
    """
    Validate snapshot creation.
    """

    snapshot = EquityCurve.calculate(
        [],
        initial_capital=100000.0,
    )

    assert snapshot.points == ()
    assert snapshot.peak_equity == 100000.0
    assert snapshot.maximum_drawdown == 0.0


def test_equity_progression() -> None:
    """
    Validate chronological equity progression.
    """

    positions = [
        _closed_position(
            pnl=1000.0,
            exit_minutes=5,
        ),
        _closed_position(
            pnl=-500.0,
            exit_minutes=10,
        ),
    ]

    snapshot = EquityCurve.calculate(
        positions,
        initial_capital=100000.0,
    )

    assert len(snapshot.points) == 2

    assert (
        snapshot.points[0].equity
        ==
        101000.0
    )

    assert (
        snapshot.points[1].equity
        ==
        100500.0
    )


def test_drawdown_calculation() -> None:
    """
    Validate maximum drawdown.
    """

    positions = [
        _closed_position(
            pnl=5000.0,
            exit_minutes=5,
        ),
        _closed_position(
            pnl=-3000.0,
            exit_minutes=10,
        ),
    ]

    snapshot = EquityCurve.calculate(
        positions,
        initial_capital=100000.0,
    )

    assert snapshot.peak_equity == 105000.0
    assert snapshot.maximum_drawdown == 3000.0
    assert snapshot.maximum_drawdown_percentage > 0.0


def test_edge_cases() -> None:
    """
    Validate empty dataset handling.
    """

    snapshot = EquityCurve.calculate(
        [],
        initial_capital=0.0,
    )

    assert snapshot.points == ()
    assert snapshot.maximum_drawdown == 0.0
    assert (
        snapshot.maximum_drawdown_percentage
        ==
        0.0
    )


def test_determinism() -> None:
    """
    Validate deterministic calculation.
    """

    positions = [
        _closed_position(
            pnl=2000.0,
            exit_minutes=5,
        ),
        _closed_position(
            pnl=-1000.0,
            exit_minutes=10,
        ),
    ]

    first = EquityCurve.calculate(
        positions,
        initial_capital=100000.0,
    )

    second = EquityCurve.calculate(
        positions,
        initial_capital=100000.0,
    )

    assert first == second


def main() -> None:

    test_equity_curve_construction()
    test_equity_progression()
    test_drawdown_calculation()
    test_edge_cases()
    test_determinism()

    print("=" * 60)
    print("Equity Curve Validation Passed")
    print("=" * 60)
    print()
    print("Construction      : OK")
    print("Equity Tracking   : OK")
    print("Drawdown          : OK")
    print("Edge Cases        : OK")
    print("Determinism       : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()