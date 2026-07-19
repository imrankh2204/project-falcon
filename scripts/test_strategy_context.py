"""
Project Falcon Strategy Context Test
"""

from datetime import datetime

from app.market.candle import Candle
from app.market.instrument import Instrument
from app.market.option_type import OptionType
from app.market.timeframe import TimeFrame
from app.strategies.context import StrategyContext


def main() -> None:
    print("=" * 50)
    print("Project Falcon Strategy Context Test")
    print("=" * 50)

    instrument = Instrument(
        exchange="NFO",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=75,
        tick_size=0.05,
        option_type=OptionType.CALL,
    )

    candle = Candle(
        timestamp=datetime.now(),
        open=100,
        high=105,
        low=99,
        close=104,
        volume=1000,
        timeframe=TimeFrame.FIVE_MINUTES,
    )

    context = StrategyContext(
        instrument=instrument,
        timeframe=TimeFrame.FIVE_MINUTES,
        candles=[candle],
    )

    print(f"Instrument : {context.instrument.symbol}")
    print(f"TimeFrame  : {context.timeframe}")
    print(f"Candles    : {len(context.candles)}")

    assert context.instrument.symbol == "NIFTY25JUL25000CE"
    assert len(context.candles) == 1

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()