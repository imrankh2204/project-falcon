"""
Project Falcon Trade Request Test
"""

from app.market.instrument import Instrument
from app.market.option_type import OptionType
from app.strategies.signal import Signal
from app.trading.trade_request import TradeRequest


def main() -> None:

    print("=" * 50)
    print("Project Falcon Trade Request Test")
    print("=" * 50)

    instrument = Instrument(
        exchange="NFO",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=75,
        tick_size=0.05,
        option_type=OptionType.CALL,
    )

    trade = TradeRequest(
        instrument=instrument,
        signal=Signal.BUY,
        quantity=75,
    )

    print(f"Instrument : {trade.instrument.symbol}")
    print(f"Signal     : {trade.signal}")
    print(f"Quantity   : {trade.quantity}")

    assert trade.signal == Signal.BUY
    assert trade.quantity == 75

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()