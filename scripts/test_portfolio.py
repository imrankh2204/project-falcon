"""
Smoke tests for the Portfolio aggregate.

Run:

    python scripts/test_portfolio.py
"""

from __future__ import annotations

from datetime import datetime

from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.portfolio import Portfolio, PortfolioError
from app.trading.position import Position


def create_position(position_id: str) -> Position:
    """
    Create a valid Position instance for testing.
    """

    instrument = Instrument(
        exchange="NSE",
        symbol="NIFTY",
        instrument_token=256265,
        lot_size=75,
        tick_size=0.05,
    )

    return Position(
        position_id=position_id,
        instrument=instrument,
        signal=Signal.BUY,
        quantity=75,
        entry_price=250.50,
        entry_time=datetime.now(),
    )


def main() -> None:
    """
    Execute portfolio smoke tests.
    """

    print("=" * 60)
    print("Portfolio Smoke Test")
    print("=" * 60)

    portfolio = Portfolio()

    print("\n[1] Verify initial portfolio state...")

    assert len(portfolio.positions) == 0
    assert portfolio.has_open_position is False
    assert portfolio.open_position is None

    print("✓ Portfolio initialized correctly")

    print("\n[2] Add first position...")

    position_one = create_position("POS-001")

    portfolio.add_position(position_one)

    assert len(portfolio.positions) == 1
    assert portfolio.has_open_position is True
    assert portfolio.open_position is position_one

    print("✓ First position accepted")

    print("\n[3] Attempt second open position...")

    position_two = create_position("POS-002")

    try:
        portfolio.add_position(position_two)
        raise AssertionError(
            "Expected PortfolioError was not raised."
        )

    except PortfolioError:
        print("✓ Second open position correctly rejected")

    print("\n[4] Verify portfolio state unchanged...")

    assert len(portfolio.positions) == 1
    assert portfolio.open_position is position_one
    assert portfolio.has_open_position is True

    print("✓ Portfolio state remained consistent")

    print("\n" + "=" * 60)
    print("All Portfolio smoke tests passed.")
    print("=" * 60)


if __name__ == "__main__":
    main()