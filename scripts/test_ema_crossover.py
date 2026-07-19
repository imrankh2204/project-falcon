"""
Project Falcon EMA Crossover Strategy Test
"""

from datetime import datetime

from app.market.candle import Candle
from app.market.instrument import Instrument
from app.market.option_type import OptionType
from app.market.timeframe import TimeFrame
from app.strategies.context import StrategyContext
from app.strategies.ema_crossover import EMACrossoverStrategy


def build(close: float) -> Candle:
    return Candle(
        timestamp=datetime.now(),
        open=close,
        high=close,
        low=close,
        close=close,
        volume=100,
        timeframe=TimeFrame.FIVE_MINUTES,
    )


def main() -> None:

    print("=" * 50)
    print("Project Falcon EMA Crossover Test")
    print("=" * 50)

    closes = list(range(100, 130))

    candles = [build(price) for price in closes]

    instrument = Instrument(
        exchange="NFO",
        symbol="NIFTY25JUL25000CE",
        instrument_token=123456,
        lot_size=75,
        tick_size=0.05,
        option_type=OptionType.CALL,
    )

    context = StrategyContext(
        instrument=instrument,
        timeframe=TimeFrame.FIVE_MINUTES,
        candles=candles,
    )

    strategy = EMACrossoverStrategy()

    signal = strategy.evaluate(context)

    print(f"Strategy : {strategy.name}")
    print(f"Signal   : {signal}")

    assert signal == signal.HOLD

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()