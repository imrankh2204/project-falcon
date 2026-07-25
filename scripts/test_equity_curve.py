"""
Equity curve validation for Project Falcon.

Validates deterministic equity curve calculation.

Validation coverage:
    - Empty datasets
    - Single profitable trade
    - Multiple trades
    - Peak equity
    - Maximum drawdown
    - Maximum drawdown percentage
    - Closed position validation
    - Deterministic output
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.backtest.equity_curve import EquityCurve
from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.position import Position


def _timestamp(offset: int) -> datetime:
    return datetime(
        2026,
        1,
        1,
        9,
        15,
        tzinfo=timezone.utc,
    ) + timedelta(minutes=offset)


def _instrument() -> Instrument:
    return Instrument(
        exchange="NSE",
        symbol="NIFTY",
        instrument_token=1,
        lot_size=50,
        tick_size=0.05,
    )


def _closed_position(
    pnl: float,
    offset: int,
) -> Position:

    entry_price = 100.0

    quantity = 50

    exit_price = entry_price + (
        pnl / quantity
    )

    position = Position(
        position_id=str(offset),
        instrument=_instrument(),
        signal=Signal.BUY,
        quantity=quantity,
        entry_price=entry_price,
        entry_time=_timestamp(offset),
    )

    position.close(
        exit_price=exit_price,
        exit_time=_timestamp(offset + 1),
    )

    return position


def test_empty_dataset() -> None:

    snapshot = EquityCurve.calculate(
        [],
        initial_capital=100000.0,
    )

    assert snapshot.points == ()

    assert snapshot.peak_equity == 100000.0

    assert snapshot.maximum_drawdown == 0.0

    assert (
        snapshot.maximum_drawdown_percentage
        == 0.0
    )


def test_single_trade() -> None:

    snapshot = EquityCurve.calculate(
        [_closed_position(1000.0, 0)],
        initial_capital=100000.0,
    )

    assert len(snapshot.points) == 1

    point = snapshot.points[0]

    assert point.equity == 101000.0

    assert snapshot.peak_equity == 101000.0

    assert snapshot.maximum_drawdown == 0.0


def test_multiple_trades() -> None:

    snapshot = EquityCurve.calculate(
        [
            _closed_position(1000.0, 0),
            _closed_position(-500.0, 2),
            _closed_position(1500.0, 4),
        ],
        initial_capital=100000.0,
    )

    assert len(snapshot.points) == 3

    assert snapshot.points[0].equity == 101000.0
    assert snapshot.points[1].equity == 100500.0
    assert snapshot.points[2].equity == 102000.0

    assert snapshot.peak_equity == 102000.0

    assert snapshot.maximum_drawdown == 500.0

    assert snapshot.maximum_drawdown_percentage > 0.0


def test_open_position_validation() -> None:

    position = Position(
        position_id="open",
        instrument=_instrument(),
        signal=Signal.BUY,
        quantity=1,
        entry_price=100.0,
        entry_time=_timestamp(0),
    )

    try:

        EquityCurve.calculate([position])

    except ValueError:

        return

    raise AssertionError(
        "Expected ValueError."
    )


def test_determinism() -> None:

    positions = [
        _closed_position(1000.0, 0),
        _closed_position(-250.0, 2),
        _closed_position(750.0, 4),
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

    test_empty_dataset()
    test_single_trade()
    test_multiple_trades()
    test_open_position_validation()
    test_determinism()

    print("=" * 60)
    print("Equity Curve Validation Passed")
    print("=" * 60)
    print()
    print("Empty Dataset     : OK")
    print("Single Trade      : OK")
    print("Multiple Trades   : OK")
    print("Drawdown          : OK")
    print("Validation        : OK")
    print("Determinism       : OK")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()