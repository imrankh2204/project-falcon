"""
Smoke tests for the Position entity.

Run:

    python scripts/test_position.py
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.market.instrument import Instrument
from app.market.option_type import OptionType
from app.strategies.signal import Signal
from app.trading.position import (
    Position,
    PositionLifecycleError,
)


def create_position(signal: Signal, entry_price: float) -> Position:
    instrument = Instrument(
        exchange="NSE",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=75,
        tick_size=0.05,
        option_type=OptionType.CALL,
    )

    return Position(
        position_id="POS-001",
        instrument=instrument,
        signal=signal,
        quantity=10,
        entry_price=entry_price,
        entry_time=datetime.now(),
    )


def main() -> None:

    print("=" * 60)
    print("Position Smoke Test")
    print("=" * 60)

    #
    # Initial state
    #

    position = create_position(
        Signal.BUY,
        100.0,
    )

    print("\n[1] Verify initial state...")

    assert position.is_open
    assert not position.is_closed

    assert position.realized_pnl == 0.0

    print("✓ Initial state verified")

    #
    # Long profit
    #

    print("\n[2] Long profit...")

    exit_time = position.entry_time + timedelta(minutes=5)

    position.close(
        exit_price=110.0,
        exit_time=exit_time,
    )

    assert position.realized_pnl == 100.0

    print("✓ Long profit verified")

    #
    # Double close
    #

    print("\n[3] Double close...")

    pnl = position.realized_pnl

    try:
        position.close(
            exit_price=120.0,
            exit_time=exit_time + timedelta(minutes=1),
        )

        raise AssertionError()

    except PositionLifecycleError:
        pass

    assert position.realized_pnl == pnl

    print("✓ Double-close rejected")

    #
    # Long loss
    #

    print("\n[4] Long loss...")

    position = create_position(
        Signal.BUY,
        110.0,
    )

    position.close(
        exit_price=100.0,
        exit_time=position.entry_time + timedelta(minutes=1),
    )

    assert position.realized_pnl == -100.0

    print("✓ Long loss verified")

    #
    # Short profit
    #

    print("\n[5] Short profit...")

    position = create_position(
        Signal.SELL,
        110.0,
    )

    position.close(
        exit_price=100.0,
        exit_time=position.entry_time + timedelta(minutes=1),
    )

    assert position.realized_pnl == 100.0

    print("✓ Short profit verified")

    #
    # Short loss
    #

    print("\n[6] Short loss...")

    position = create_position(
        Signal.SELL,
        100.0,
    )

    position.close(
        exit_price=110.0,
        exit_time=position.entry_time + timedelta(minutes=1),
    )

    assert position.realized_pnl == -100.0

    print("✓ Short loss verified")

    print("\n" + "=" * 60)
    print("All Position smoke tests passed.")
    print("=" * 60)


if __name__ == "__main__":
    main()