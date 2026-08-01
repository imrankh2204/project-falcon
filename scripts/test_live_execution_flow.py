"""
Project-Falcon

FAL-520-R3.2

Live execution flow validation.

Validates:

TradeRequest
      |
      v
LiveExecutionEngine
      |
      v
OrderRequest
      |
      v
LiveTradingService
      |
      v
Mock BrokerGateway
      |
      v
ExecutionResult
"""

from app.live.broker_gateway import BrokerGateway
from app.live.execution_result import ExecutionResult
from app.live.live_execution_engine import (
    LiveExecutionEngine,
)
from app.live.live_trading_service import (
    LiveTradingService,
)
from app.live.order import Order
from app.live.order_id import OrderId
from app.live.order_status import OrderStatus
from app.market.instrument import Instrument
from app.portfolio.synchronization_service import (
    PortfolioSynchronizationService,
)
from app.strategies.signal import Signal
from app.trading.risk_manager import RiskManager
from app.trading.trade_request import TradeRequest


# ---------------------------------------------------------
# Mock Broker Gateway
# ---------------------------------------------------------


class MockBrokerGateway(BrokerGateway):

    def __init__(self):
        self.order_received = None

    def authenticate(self):
        return None

    def session(self):
        return None

    def logout(self):
        pass

    def place_order(
        self,
        order_request,
    ):
        from datetime import datetime

        self.order_received = order_request

        now = datetime.now()

        return Order(
            order_id=OrderId(
                "TEST-001"
            ),
            instrument=order_request.instrument,
            transaction_type=order_request.transaction_type,
            order_type=order_request.order_type,
            product_type=order_request.product_type,
            status=OrderStatus.FILLED,
            quantity=order_request.quantity,
            filled_quantity=order_request.quantity,
            average_price=100.0,
            price=100.0,
            trigger_price=None,
            created_at=now,
            updated_at=now,
        )

        return ExecutionResult(
            order=order,
            accepted=True,
            message="Mock execution successful",
        )

    def cancel_order(
        self,
        order_id,
    ):
        return None

    def get_order(
        self,
        order_id,
    ):
        return None

    def orders(self):
        return ()

    def positions(self):
        return ()

    def quote(
        self,
        instrument,
    ):
        return None


# ---------------------------------------------------------
# Mock Risk Manager
# ---------------------------------------------------------


class MockRiskManager(RiskManager):

    def validate(
        self,
        order_request,
    ):
        return True


# ---------------------------------------------------------
# Mock Portfolio Synchronization
# ---------------------------------------------------------


class MockSynchronizationService(
    PortfolioSynchronizationService
):

    def __init__(
        self,
        broker_gateway,
    ):
        super().__init__(
            broker_gateway=broker_gateway
        )

    def synchronize(self):
        pass


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------


def main():

    broker = MockBrokerGateway()

    risk = MockRiskManager()

    synchronization = (
        MockSynchronizationService(
            broker_gateway=broker
        )
    )

    live_service = LiveTradingService(
        broker_gateway=broker,
        risk_manager=risk,
        synchronization_service=synchronization,
    )

    execution_engine = LiveExecutionEngine(
        live_trading_service=live_service,
    )


    print(
        "PASS: LiveExecutionEngine initialized"
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


    trade_request = TradeRequest(
        instrument=instrument,
        signal=Signal.BUY,
        quantity=50,
    )


    result = execution_engine.execute(
        trade_request
    )

    print(type(result))

    print(result)

    assert isinstance(
        result,
        ExecutionResult,
    )

    assert (
        broker.order_received
        is not None
    )


    print(
        "PASS: TradeRequest converted"
    )

    print(
        "PASS: Order submitted through BrokerGateway"
    )

    print(
        "PASS: ExecutionResult returned"
    )

    print()

    print(
        "FAL-520-R3.2 COMPLETE"
    )


if __name__ == "__main__":
    main()