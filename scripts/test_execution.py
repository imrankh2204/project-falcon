"""
Smoke test for PaperExecutionEngine.

Run:

    python scripts/test_execution.py
"""

from __future__ import annotations

from app.market.instrument import Instrument
from app.strategies.signal import Signal
from app.trading.execution import PaperExecutionEngine
from app.trading.trade_request import TradeRequest


def main() -> None:
    print("=" * 50)
    print("Project Falcon - PaperExecutionEngine Test")
    print("=" * 50)

    instrument = Instrument(
        exchange="NFO",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=50,
        tick_size=0.05,
    )

    request = TradeRequest(
        instrument=instrument,
        signal=Signal.BUY,
        quantity=50,
    )

    engine = PaperExecutionEngine()

    position = engine.execute(
        request=request,
        execution_price=245.60,
    )

    assert position.instrument == request.instrument
    assert position.signal == request.signal
    assert position.quantity == request.quantity
    assert position.entry_price == 245.60
    assert position.entry_time is not None
    assert position.is_open
    assert not position.is_closed
    assert position.position_id

    print("[PASS] Position created successfully")
    print(f"[PASS] Instrument : {position.instrument.display_name}")
    print(f"[PASS] Signal     : {position.signal}")
    print(f"[PASS] Quantity   : {position.quantity}")
    print(f"[PASS] Entry Price: {position.entry_price}")
    print(f"[PASS] Entry Time : {position.entry_time}")
    print(f"[PASS] Position ID : {position.position_id}")

    print("\nAll PaperExecutionEngine tests passed.")


if __name__ == "__main__":
    main()