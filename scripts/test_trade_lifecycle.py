"""
End-to-end lifecycle validation for Project Falcon.

Run:

    python scripts/test_trade_lifecycle.py
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.execution import PaperExecutionEngine
from app.trading.portfolio import Portfolio
from app.trading.risk_manager import RiskManager
from app.trading.trade_request import TradeRequest
from app.trading.trading_service import TradingService


def main() -> None:
    print("=" * 60)
    print("Project Falcon - End-to-End Lifecycle Test")
    print("=" * 60)

    instrument = Instrument(
        exchange="NFO",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=50,
        tick_size=0.05,
    )

    portfolio = Portfolio()
    risk_manager = RiskManager()
    execution_engine = PaperExecutionEngine()

    trading_service = TradingService(
        risk_manager=risk_manager,
        execution_engine=execution_engine,
        portfolio=portfolio,
    )

    print()
    print("[1] Verify initial portfolio state...")

    assert not portfolio.has_open_position
    assert portfolio.open_position is None
    assert len(portfolio.positions) == 0

    print("✓ Initial portfolio verified")

    print()
    print("[2] Submit first trade...")

    first_trade = TradeRequest(
        instrument=instrument,
        signal=Signal.BUY,
        quantity=50,
    )

    first_position = trading_service.submit_trade(
        first_trade,
        execution_price=250.50,
        trades_today=0,
    )

    assert portfolio.has_open_position
    assert portfolio.open_position is first_position
    assert first_position.is_open

    print("✓ First trade executed")

    print()
    print("[3] Close first position...")

    first_position.close(
        exit_price=255.75,
        exit_time=first_position.entry_time + timedelta(minutes=5),
    )

    assert first_position.is_closed
    assert not portfolio.has_open_position
    assert portfolio.open_position is None

    print("✓ First position closed")

    print()
    print("[4] Submit second trade...")

    second_trade = TradeRequest(
        instrument=instrument,
        signal=Signal.BUY,
        quantity=50,
    )

    second_position = trading_service.submit_trade(
        second_trade,
        execution_price=260.25,
        trades_today=1,
    )

    assert second_position.is_open
    assert portfolio.has_open_position
    assert portfolio.open_position is second_position

    print("✓ Second trade executed")

    print()
    print("[5] Verify portfolio history...")

    assert len(portfolio.positions) == 2

    positions = list(portfolio.positions.values())

    assert positions[0].is_closed
    assert positions[1].is_open

    print("✓ Portfolio history verified")

    print()
    print("=" * 60)
    print("End-to-End Lifecycle Validation Passed")
    print("=" * 60)


if __name__ == "__main__":
    main()