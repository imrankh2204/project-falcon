"""
Project Falcon

FAL-540-R2

Integrated Paper Trade Validation

Validates the complete paper trading execution pipeline using the
production runtime components.

Pipeline

Market Event
      |
      v
LiveRuntime
      |
      v
LiveEngine
      |
      v
Strategy Engine
      |
      v
TradeSignalTranslator
      |
      v
TradeRequest
      |
      v
LiveExecutionEngine
      |
      v
LiveTradingService
      |
      v
PaperBrokerGateway
      |
      v
ExecutionResult
"""

from __future__ import annotations

from datetime import datetime
from app.live.quote import Quote
from app.live.execution_result import ExecutionResult
from app.live.live_engine import LiveEngine
from app.live.live_execution_engine import LiveExecutionEngine
from app.live.live_runtime import LiveRuntime
from app.live.live_trading_service import LiveTradingService
from app.market.instrument import Instrument
from app.paper.paper_broker_gateway import PaperBrokerGateway
from app.portfolio.synchronization_service import (
    PortfolioSynchronizationService,
)
from app.services.trade_signal_translator import (
    TradeSignalTranslator,
)
from app.strategies.signal import Signal
from app.trading.risk_manager import RiskManager


# ---------------------------------------------------------
# Strategy
# ---------------------------------------------------------


class MockStrategyEngine:

    def __init__(
        self,
        instrument: Instrument,
    ):
        self._instrument = instrument

    def evaluate(
        self,
        event,
    ):
        return {
            self._instrument: Signal.BUY,
        }


# ---------------------------------------------------------
# Event Source
# ---------------------------------------------------------


class MockEventSource:

    def start(self):
        pass

    def stop(self):
        pass


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------


def main():

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

    #
    # Production components
    #

    broker_gateway = PaperBrokerGateway()

    broker_gateway.authenticate()

    broker_gateway.update_quote(
        Quote(
            instrument=instrument,
            last_price=25000.0,
            bid=24999.5,
            ask=25000.5,
            volume=1000,
            timestamp=datetime.now(),
        )
    )

    synchronization_service = (
        PortfolioSynchronizationService(
            broker_gateway=broker_gateway,
        )
    )

    risk_manager = RiskManager()

    live_trading_service = LiveTradingService(
        broker_gateway=broker_gateway,
        risk_manager=risk_manager,
        synchronization_service=synchronization_service,
    )

    execution_engine = LiveExecutionEngine(
        live_trading_service=live_trading_service,
    )

    runtime = LiveRuntime(
        live_engine=LiveEngine(
            strategy_engine=MockStrategyEngine(
                instrument,
            ),
            trading_service=execution_engine,
            signal_translator=TradeSignalTranslator(
                default_quantity=instrument.lot_size,
            ),
            risk_manager=risk_manager,
        ),
        event_source=MockEventSource(),
    )

    runtime.start()

    print("PASS: Runtime started")

    result = runtime.process_event(
        {
            "timestamp": "now",
        }
    )

    assert isinstance(
        result,
        ExecutionResult,
    )

    assert result.accepted is True

    assert (
        result.order.instrument
        == instrument
    )

    assert (
        result.order.filled_quantity
        == 50
    )

    assert (
        result.order.average_price
        == 25000.0
    )

    print("PASS: Strategy evaluated")

    print("PASS: Order executed")

    print("PASS: ExecutionResult returned")

    runtime.stop()

    print("PASS: Runtime stopped")

    print()

    print("FAL-540-R2 COMPLETE")


if __name__ == "__main__":
    main()