"""
Smoke tests for the Portfolio aggregate.

Run:

    python scripts/test_portfolio.py
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.portfolio import Portfolio, PortfolioError
from app.trading.position import Position


def create_position(
    position_id: str,
    signal: Signal,
    entry_price: float,
) -> Position:
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
        signal=signal,
        quantity=10,
        entry_price=entry_price,
        entry_time=datetime.now(),
    )


def close_position(
    position: Position,
    exit_price: float,
) -> None:
    """
    Close a position using a valid exit timestamp.
    """

    position.close(
        exit_price=exit_price,
        exit_time=position.entry_time + timedelta(minutes=5),
    )


def main() -> None:
    """
    Execute portfolio smoke tests.
    """

    print("=" * 60)
    print("Portfolio Smoke Test")
    print("=" * 60)

    #
    # Initial state
    #

    portfolio = Portfolio()

    print("\n[1] Verify initial portfolio state...")

    assert len(portfolio.positions) == 0
    assert portfolio.has_open_position is False
    assert portfolio.open_position is None

    assert portfolio.total_realized_pnl == 0.0
    assert portfolio.closed_position_count == 0
    assert portfolio.winning_position_count == 0
    assert portfolio.losing_position_count == 0
    assert portfolio.breakeven_position_count == 0

    print("✓ Initial portfolio state verified")

    #
    # Winning position
    #

    print("\n[2] Verify winning position accounting...")

    winner = create_position(
        "POS-001",
        Signal.BUY,
        100.0,
    )

    portfolio.add_position(winner)

    close_position(
        winner,
        110.0,
    )

    assert portfolio.total_realized_pnl == 100.0
    assert portfolio.closed_position_count == 1
    assert portfolio.winning_position_count == 1
    assert portfolio.losing_position_count == 0
    assert portfolio.breakeven_position_count == 0

    print("✓ Winning trade accounting verified")

    #
    # Losing position
    #

    print("\n[3] Verify losing position accounting...")

    loser = create_position(
        "POS-002",
        Signal.BUY,
        120.0,
    )

    portfolio.add_position(loser)

    close_position(
        loser,
        110.0,
    )

    assert portfolio.total_realized_pnl == 0.0
    assert portfolio.closed_position_count == 2
    assert portfolio.winning_position_count == 1
    assert portfolio.losing_position_count == 1
    assert portfolio.breakeven_position_count == 0

    print("✓ Losing trade accounting verified")

    #
    # Breakeven position
    #

    print("\n[4] Verify breakeven accounting...")

    breakeven = create_position(
        "POS-003",
        Signal.BUY,
        150.0,
    )

    portfolio.add_position(breakeven)

    close_position(
        breakeven,
        150.0,
    )

    assert portfolio.total_realized_pnl == 0.0
    assert portfolio.closed_position_count == 3
    assert portfolio.winning_position_count == 1
    assert portfolio.losing_position_count == 1
    assert portfolio.breakeven_position_count == 1

    print("✓ Breakeven accounting verified")

    #
    # Single-open-position rule
    #

    print("\n[5] Verify open-position constraint...")

    open_position = create_position(
        "POS-004",
        Signal.BUY,
        100.0,
    )

    portfolio.add_position(open_position)

    duplicate = create_position(
        "POS-005",
        Signal.BUY,
        100.0,
    )

    try:
        portfolio.add_position(duplicate)
        raise AssertionError(
            "Expected PortfolioError was not raised."
        )

    except PortfolioError:
        print("✓ Second open position rejected")

    #
    # Open position excluded from accounting
    #

    print("\n[6] Verify open position exclusion...")

    assert portfolio.total_realized_pnl == 0.0
    assert portfolio.closed_position_count == 3
    assert portfolio.winning_position_count == 1
    assert portfolio.losing_position_count == 1
    assert portfolio.breakeven_position_count == 1

    print("✓ Open position excluded from accounting")

    #
    # Average winner analytics
    #

    print("\n[7] Verify average winner analytics...")

    assert portfolio.average_winning_pnl == 100.0

    print("✓ Average winner analytics verified")

    #
    # Average loser analytics
    #

    print("\n[8] Verify average loser analytics...")

    assert portfolio.average_losing_pnl == -100.0

    print("✓ Average loser analytics verified")

    #
    # Empty analytics
    #

    print("\n[9] Verify empty analytics...")

    empty_portfolio = Portfolio()

    assert empty_portfolio.average_winning_pnl == 0.0
    assert empty_portfolio.average_losing_pnl == 0.0

    print("✓ Empty analytics verified")

    #
    # Profit factor
    #

    print("\n[10] Verify profit factor...")

    #
    # Existing portfolio:
    #
    # Winner   +100
    # Loser    -100
    # Breakeven   0
    #
    # Profit Factor = 100 / 100 = 1.0
    #

    assert portfolio.profit_factor == 1.0

    print("✓ Profit factor verified")

    #
    # Winners only
    #

    print("\n[11] Verify infinite profit factor...")

    winners_only = Portfolio()

    winner = create_position(
        "POS-100",
        Signal.BUY,
        100.0,
    )

    winners_only.add_position(winner)

    close_position(
        winner,
        110.0,
    )

    assert winners_only.profit_factor == float("inf")

    print("✓ Infinite profit factor verified")

    #
    # Losers only
    #

    print("\n[12] Verify zero profit factor...")

    losers_only = Portfolio()

    loser = create_position(
        "POS-101",
        Signal.BUY,
        120.0,
    )

    losers_only.add_position(loser)

    close_position(
        loser,
        110.0,
    )

    assert losers_only.profit_factor == 0.0

    print("✓ Zero profit factor verified")

    #
    # Empty portfolio
    #

    print("\n[13] Verify empty portfolio profit factor...")

    empty = Portfolio()

    assert empty.profit_factor == 0.0

    print("✓ Empty portfolio profit factor verified")
    
    print("\n" + "=" * 60)
    print("All Portfolio smoke tests passed.")
    print("=" * 60)

if __name__ == "__main__":
    main()