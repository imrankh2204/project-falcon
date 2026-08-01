"""
Execution refresh service.

Coordinates refreshing live execution state while remaining broker
independent.

Responsibilities
----------------
- Refresh active broker orders.
- Coordinate OrderMonitor.
- Return immutable order snapshots.

The service intentionally does NOT implement:

- Scheduling
- Polling loops
- Retry logic
- Persistence
- Event publishing
- Broker communication
"""

from __future__ import annotations

from app.live.order import (
    Order,
)
from app.live.order_monitor import (
    OrderMonitor,
)


class ExecutionRefreshService:
    """
    Coordinates execution refresh operations.
    """

    def __init__(
        self,
        *,
        order_monitor: OrderMonitor,
    ) -> None:
        """
        Initialize the execution refresh service.
        """

        if not isinstance(
            order_monitor,
            OrderMonitor,
        ):
            raise TypeError(
                "order_monitor must be an OrderMonitor."
            )

        self._order_monitor = order_monitor

    @property
    def order_monitor(
        self,
    ) -> OrderMonitor:
        """
        Return the configured order monitor.
        """

        return self._order_monitor

    def refresh(
        self,
    ) -> tuple[
        Order,
        ...,
    ]:
        """
        Refresh active broker orders.

        Returns
        -------
        tuple[Order, ...]
            Immutable active broker orders.
        """

        return self._order_monitor.active_orders()