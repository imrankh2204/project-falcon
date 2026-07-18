"""
Project Falcon Market Domain Validation
"""

from datetime import date, datetime

from app.market.candle import Candle
from app.market.instrument import Instrument
from app.market.option_type import OptionType
from app.market.timeframe import TimeFrame


def main() -> None:
    print("=" * 50)
    print("Project Falcon Market Domain Test")
    print("=" * 50)

    timeframe = TimeFrame.FIVE_MINUTES

    candle = Candle(
        timestamp=datetime(2026, 7, 18, 9, 15),
        open=25000.0,
        high=25040.5,
        low=24990.2,
        close=25032.8,
        volume=125000,
        timeframe=timeframe,
    )

    instrument = Instrument(
        exchange="NFO",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=75,
        tick_size=0.05,
        expiry=date(2026, 7, 30),
        strike=25000.0,
        option_type=OptionType.CALL,
    )

    print(f"Instrument : {instrument.display_name}")
    print(f"TimeFrame  : {candle.timeframe}")
    print(f"Bullish    : {candle.is_bullish}")
    print(f"Option     : {instrument.is_option}")

    assert candle.timeframe is TimeFrame.FIVE_MINUTES
    assert instrument.option_type is OptionType.CALL
    assert instrument.is_option
    assert candle.is_bullish

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()