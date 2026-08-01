"""
Project Falcon

FAL-530-R2

End-to-End Paper Runtime Validation

Validates:

Market Event
      |
      v
LiveRuntime
      |
      v
LiveEngine
      |
      v
LiveExecutionEngine
      |
      v
LiveTradingService
      |
      v
PaperBrokerGateway
"""

from __future__ import annotations

from datetime import datetime

from app.live.quote import Quote
from app.market.instrument import Instrument
from app.paper.paper_broker_gateway import (
    PaperBrokerGateway,
)
from app.paper.paper_runtime_factory import (
    PaperRuntimeFactory,
)
from app.strategies.signal import Signal
from app.trading.risk_manager import RiskManager
from app.trading.trade_request import TradeRequest


# ---------------------------------------------------------
# Test doubles
# ---------------------------------------------------------


class MockStrategyEngine:
    def evaluate(
        self,
        event,
    ):
        return {
            event["instrument"]: "BUY",
        }


class MockSignalTranslator:
    def translate(
        self,
        instrument,
        signal,
    ):
        return TradeRequest(
            instrument=instrument,
            signal=Signal.BUY,
            quantity=50,
        )


class MockMarketFeed:
    def start(self):
        pass

    def stop(self):
        pass


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------


def main() -> None:

    strategy = MockStrategyEngine()

    translator = MockSignalTranslator()

    risk = RiskManager()

    market_feed = MockMarketFeed()

    factory = PaperRuntimeFactory()

    runtime = factory.create(
        strategy_engine=strategy,
        signal_translator=translator,
        risk_manager=risk,
        market_feed=market_feed,
    )

    #
    # Obtain the real PaperBrokerGateway.
    #
    broker = (
        runtime.live_engine
        .trading_service
        ._live_trading_service
        ._broker_gateway
    )

    assert isinstance(
        broker,
        PaperBrokerGateway,
    )

    print(
        "PASS: Runtime created"
    )

    instrument = Instrument(
        exchange="NFO",
        symbol="NIFTY",
        instrument_token=1,
        lot_size=50,
        tick_size=0.05,
        expiry=None,
        strike=25000,
        option_type=None,
    )

    broker.update_quote(
        Quote(
            instrument=instrument,
            last_price=250.50,
            bid=250.45,
            ask=250.55,
            volume=1000,
            timestamp=datetime.now(),
        )
    )

    runtime.start()

    print(
        "PASS: Runtime started"
    )

    runtime.process_event(
        {
            "instrument": instrument,
        }
    )

    orders = broker.orders()

    assert len(
        orders
    ) == 1

    order = orders[0]

    assert (
        order.quantity == 50
    )

    assert (
        order.average_price == 250.50
    )

    print(
        "PASS: Paper order created"
    )

    runtime.stop()

    print(
        "PASS: Runtime stopped"
    )

    print()

    print(
        "FAL-530-R2 COMPLETE"
    )


if __name__ == "__main__":
    main()