"""
Project Falcon

FAL-560-R3

Runtime Diagnostics Validation
"""

from __future__ import annotations

from datetime import datetime

from app.live.execution_result import ExecutionResult
from app.live.live_runtime import LiveRuntime
from app.live.order import Order
from app.live.order_id import OrderId
from app.live.order_status import OrderStatus
from app.live.runtime_event import RuntimeEvent
from app.live.runtime_statistics import RuntimeStatistics
from app.live.transaction_type import TransactionType
from app.live.order_type import OrderType
from app.live.product_type import ProductType
from app.market.instrument import Instrument


class MockEngine:

    def start(self):
        pass

    def stop(self):
        pass

    def process_event(self, event):

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

        order = Order(
            order_id=OrderId("TEST-1"),
            instrument=instrument,
            transaction_type=TransactionType.BUY,
            order_type=OrderType.MARKET,
            product_type=ProductType.MIS,
            status=OrderStatus.FILLED,
            quantity=50,
            filled_quantity=50,
            average_price=25000.0,
            price=25000.0,
            trigger_price=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return ExecutionResult(
            order=order,
            accepted=True,
        )


class MockEventSource:

    def start(self):
        pass

    def stop(self):
        pass

    def events(self):
        yield {}
        yield {}
        yield {}


def main():

    runtime = LiveRuntime(
        live_engine=MockEngine(),
        event_source=MockEventSource(),
    )

    runtime.run()

    stats = runtime.statistics()
    events = runtime.events()

    assert isinstance(
        stats,
        RuntimeStatistics,
    )

    assert isinstance(
        events,
        tuple,
    )

    assert len(events) == 3

    assert stats.events_processed == 3

    assert stats.accepted_trades == 3

    assert stats.rejected_trades == 0

    assert isinstance(
        events[0],
        RuntimeEvent,
    )

    assert events[0].sequence == 1
    assert events[1].sequence == 2
    assert events[2].sequence == 3

    print("PASS: RuntimeStatistics verified")
    print("PASS: RuntimeEvent history verified")
    print("PASS: Event ordering verified")
    print("PASS: Immutable diagnostics verified")
    print()
    print("FAL-560-R3 COMPLETE")


if __name__ == "__main__":
    main()