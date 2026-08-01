"""
Project-Falcon
FAL-520-R3

End-to-End Live Runtime Flow Validation

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
Strategy
      |
      v
Translator
      |
      v
Risk
      |
      v
TradingService
"""

from app.live.live_engine import LiveEngine
from app.live.live_runtime import LiveRuntime


# ---------------------------------------------------------
# Test Doubles
# ---------------------------------------------------------


class MockStrategyEngine:
    def __init__(self):
        self.called = False

    def evaluate(self, event):
        self.called = True

        return {
            "NIFTY": "BUY"
        }


class MockSignalTranslator:
    def __init__(self):
        self.called = False

    def translate(self, signal):
        self.called = True

        return {
            "symbol": "NIFTY",
            "action": signal,
        }


class MockRiskManager:
    def __init__(self):
        self.called = False

    def validate(self, trade_request):
        self.called = True

        return True


class MockTradingService:
    def __init__(self):
        self.called = False
        self.trade = None

    def submit_trade(self, trade_request):
        self.called = True
        self.trade = trade_request

        return trade_request


class MockEventSource:
    def __init__(self):
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------


def main():

    strategy = MockStrategyEngine()

    translator = MockSignalTranslator()

    risk = MockRiskManager()

    trading_service = MockTradingService()

    engine = LiveEngine(
        strategy_engine=strategy,
        trading_service=trading_service,
        signal_translator=translator,
        risk_manager=risk,
    )

    event_source = MockEventSource()

    runtime = LiveRuntime(
        live_engine=engine,
        event_source=event_source,
    )


    print("PASS: LiveRuntime initialized")


    runtime.start()

    assert runtime.running is True
    assert engine.running is True
    assert event_source.started is True

    print("PASS: Runtime started")


    result = runtime.process_event(
        {
            "symbol": "NIFTY",
            "price": 25000,
        }
    )


    assert strategy.called is True
    assert translator.called is True
    assert risk.called is True
    assert trading_service.called is True
    assert result is not None

    print("PASS: Market event processed")

    print("PASS: Trade request submitted")


    runtime.stop()


    assert runtime.running is False
    assert engine.running is False
    assert event_source.stopped is True

    print("PASS: Runtime stopped")

    print()
    print("FAL-520-R3 COMPLETE")


if __name__ == "__main__":
    main()