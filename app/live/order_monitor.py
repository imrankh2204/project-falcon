"""
Live order monitoring service.

Provides broker-independent read access to broker orders.

Responsibilities
----------------
- Retrieve a single broker order.
- Retrieve all broker orders.
- Remain broker independent.
- Return immutable domain objects.

The service intentionally does NOT implement:

- Order placement
- Order cancellation
- Order modification
- Order filtering
- Retry logic
- Scheduling
- Persistence
"""

from __future__ import annotations

from app.live.broker_gateway import (
    BrokerGateway,
)
from app.live.order import (
    Order,
)
from app.live.order_id import (
    OrderId,
)
from app.live.order_status import (
    OrderStatus,
)

class OrderMonitor:
    """
    Read-only service for monitoring broker orders.
    """

    def __init__(
        self,
        *,
        broker_gateway: BrokerGateway,
    ) -> None:
        """
        Initialize the order monitor.
        """

        if not isinstance(
            broker_gateway,
            BrokerGateway,
        ):
            raise TypeError(
                "broker_gateway must be a BrokerGateway."
            )

        self._broker_gateway = broker_gateway

    @property
    def broker_gateway(
        self,
    ) -> BrokerGateway:
        """
        Return the configured broker gateway.
        """

        return self._broker_gateway

    def order(
        self,
        order_id: OrderId,
    ) -> Order:
        """
        Retrieve a broker order.

        Parameters
        ----------
        order_id
            Broker order identifier.

        Returns
        -------
        Order
            Immutable broker order.
        """

        if not isinstance(
            order_id,
            OrderId,
        ):
            raise TypeError(
                "order_id must be an OrderId."
            )

        return self._broker_gateway.get_order(
            order_id,
        )

    def orders(
        self,
    ) -> tuple[
        Order,
        ...,
    ]:
        """
        Retrieve all broker orders.

        Returns
        -------
        tuple[Order, ...]
            Immutable broker orders.
        """

        return self._broker_gateway.orders()

    def active_orders(
        self,
    ) -> tuple[
        Order,
        ...,
    ]:
        """
        Retrieve active broker orders.

        Returns
        -------
        tuple[Order, ...]
            Immutable active broker orders.
        """

        return tuple(
            order
            for order in self.orders()
            if order.status in (
                OrderStatus.NEW,
                OrderStatus.OPEN,
                OrderStatus.PARTIALLY_FILLED,
            )
        )