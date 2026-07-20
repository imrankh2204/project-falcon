"""
Smoke test for TradingService.
"""

from __future__ import annotations

from app.market.instrument import Instrument
from app.trading.execution import PaperExecutionEngine
from app.trading.portfolio import Portfolio
from app.trading.risk_manager import RiskManager
from app.trading.trade_request import TradeRequest
from app.trading.trading_service import TradingService


def main() -> None:
    print("=" * 60)
    print("TradingService Smoke Test")
    print("=" * 60)

    instrument = Instrument(
        exchange="NSE",
        symbol="NIFTY",
        instrument_token=12345,
        lot_size=50,
        tick_size=0.05,
    )

    trade = TradeRequest(
        instrument=instrument,
        signal="Signal.BUY",
        quantity=50,
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
    print("[1] Submit first trade...")

    position = trading_service.submit_trade(
        trade,
        execution_price=250.50,
        trades_today=0,
    )

    assert position.is_open
    assert portfolio.has_open_position
    assert portfolio.open_position is position

    print("✓ First trade executed successfully")

    print()
    print("[2] Attempt second trade...")

    second_trade = TradeRequest(
        instrument=instrument,
        signal="Signal.BUY",
        quantity=50,
    )

    try:
        trading_service.submit_trade(
            second_trade,
            execution_price=251.25,
            trades_today=1,
        )

        raise AssertionError(
            "Expected second open position to be rejected."
        )

    except ValueError:
        print("✓ Second trade correctly rejected")

    print()
    print("[3] Verify portfolio consistency...")

    assert portfolio.has_open_position
    assert portfolio.open_position is position

    print("✓ Portfolio state remained consistent")

    print()
    print("=" * 60)
    print("All TradingService smoke tests passed.")
    print("=" * 60)


if __name__ == "__main__":
    main()