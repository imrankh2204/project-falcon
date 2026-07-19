"""
Project Falcon Risk Manager Test
"""

from datetime import datetime

from app.market.instrument import Instrument
from app.market.option_type import OptionType
from app.strategies.signal import Signal
from app.trading.position import Position
from app.trading.risk_manager import RiskManager
from app.trading.trade_request import TradeRequest


def instrument() -> Instrument:
    return Instrument(
        exchange="NFO",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=75,
        tick_size=0.05,
        option_type=OptionType.CALL,
    )


def request() -> TradeRequest:
    return TradeRequest(
        instrument=instrument(),
        signal=Signal.BUY,
        quantity=75,
    )


def position() -> Position:
    return Position(
        instrument=instrument(),
        signal=Signal.BUY,
        quantity=75,
        entry_price=250.50,
        entry_time=datetime.now(),
    )


def main() -> None:

    print("=" * 50)
    print("Project Falcon Risk Manager Test")
    print("=" * 50)

    risk = RiskManager()

    print("\nScenario 1 : Valid Trade")
    approved = risk.approve(
        request(),
        open_positions=[],
        trades_today=0,
    )
    print(f"Approved : {approved}")
    assert approved

    print("\nScenario 2 : Open Position Limit")
    approved = risk.approve(
        request(),
        open_positions=[position()],
        trades_today=0,
    )
    print(f"Approved : {approved}")
    assert not approved

    print("\nScenario 3 : Daily Trade Limit")
    approved = risk.approve(
        request(),
        open_positions=[],
        trades_today=3,
    )
    print(f"Approved : {approved}")
    assert not approved

    print("\nScenario 4 : Invalid Quantity")
    invalid = TradeRequest(
        instrument=instrument(),
        signal=Signal.BUY,
        quantity=0,
    )

    approved = risk.approve(
        invalid,
        open_positions=[],
        trades_today=0,
    )

    print(f"Approved : {approved}")
    assert not approved

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()