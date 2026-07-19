"""
Project Falcon Strategy Engine Test
"""

from datetime import datetime

from app.market.candle import Candle
from app.market.instrument import Instrument
from app.market.option_type import OptionType
from app.market.timeframe import TimeFrame
from app.strategies.context import StrategyContext
from app.strategies.ema_crossover import EMACrossoverStrategy
from app.strategies.engine import StrategyEngine
from app.strategies.signal import Signal


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
    print("Project Falcon Strategy Engine Test")
    print("=" * 50)

    candles = [build(price) for price in range(100, 130)]

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

    engine = StrategyEngine(
        [
            EMACrossoverStrategy(),
        ]
    )

    results = engine.evaluate(context)

    print(f"Strategies : {engine.strategy_count}")

    for name, signal in results.items():
        print(f"{name} -> {signal}")

    assert engine.strategy_count == 1

    assert (
        results["EMA Crossover (9/21)"]
        == Signal.HOLD
    )

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()