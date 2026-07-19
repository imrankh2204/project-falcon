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


def create_position() -> Position:
    """
    Create a valid Position instance for testing.
    """

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
        signal=Signal.BUY,
        quantity=75,
        entry_price=250.50,
        entry_time=datetime.now(),
    )


def main() -> None:
    """
    Execute Position smoke tests.
    """

    print("=" * 60)
    print("Position Smoke Test")
    print("=" * 60)

    position = create_position()

    print("\n[1] Verify initial state...")

    assert position.is_open is True
    assert position.is_closed is False

    assert position.exit_price is None
    assert position.exit_time is None

    print("✓ Initial state verified")

    print("\n[2] Close position...")

    exit_time = position.entry_time + timedelta(minutes=5)

    position.close(
        exit_price=255.75,
        exit_time=exit_time,
    )

    assert position.is_open is False
    assert position.is_closed is True

    assert position.exit_price == 255.75
    assert position.exit_time == exit_time

    print("✓ Position closed successfully")
    
    print("\n[3] Attempt to close position again...")

    original_exit_price = position.exit_price
    original_exit_time = position.exit_time

    try:
        position.close(
            exit_price=260.00,
            exit_time=exit_time + timedelta(minutes=1),
        )
        raise AssertionError(
            "Expected PositionLifecycleError was not raised."
        )

    except PositionLifecycleError:
        print("✓ Double-close correctly rejected")

    print("\n[4] Verify state remained unchanged...")

    assert position.is_closed is True
    assert position.is_open is False

    assert position.exit_price == original_exit_price
    assert position.exit_time == original_exit_time

    print("✓ Position state remained consistent")

    print("\n" + "=" * 60)
    print("All Position smoke tests passed.")
    print("=" * 60)


if __name__ == "__main__":
    main()