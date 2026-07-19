"""
Project Falcon Position Test
"""

from datetime import datetime

from app.market.instrument import Instrument
from app.market.option_type import OptionType
from app.strategies.signal import Signal
from app.trading.position import Position
from app.trading.position_status import PositionStatus


def main() -> None:

    print("=" * 50)
    print("Project Falcon Position Test")
    print("=" * 50)

    instrument = Instrument(
        exchange="NFO",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=75,
        tick_size=0.05,
        option_type=OptionType.CALL,
    )

    position = Position(
        instrument=instrument,
        signal=Signal.BUY,
        quantity=75,
        entry_price=250.50,
        entry_time=datetime.now(),
    )

    print(f"Instrument : {position.instrument.symbol}")
    print(f"Signal     : {position.signal}")
    print(f"Quantity   : {position.quantity}")
    print(f"Status     : {position.status}")
    print(f"Open       : {position.is_open}")

    assert position.status == PositionStatus.OPEN
    assert position.is_open
    assert not position.is_closed

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()