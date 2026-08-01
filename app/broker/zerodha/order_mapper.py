"""
Maps Falcon OrderRequest objects into Kite place_order payloads.

Responsibilities
----------------
- Translate broker-independent OrderRequest objects.
- Produce Kite-compatible payload dictionaries.
- Delegate enum conversion to dedicated mapper classes.

The mapper intentionally does NOT implement:

- Order placement
- Broker communication
- Validation beyond transport integrity
"""

from __future__ import annotations

from typing import Any

from app.broker.zerodha.order_type_mapper import (
    OrderTypeMapper,
)
from app.broker.zerodha.product_mapper import (
    ProductMapper,
)
from app.broker.zerodha.transaction_mapper import (
    TransactionMapper,
)
from app.live.order_request import (
    OrderRequest,
)


class OrderMapper:
    """
    Translate Falcon OrderRequest into Kite payload.
    """

    @classmethod
    def to_kite(
        cls,
        request: OrderRequest,
    ) -> dict[str, Any]:
        """
        Convert an OrderRequest into the payload expected by
        KiteConnect.place_order().
        """

        if not isinstance(
            request,
            OrderRequest,
        ):
            raise TypeError(
                "request must be an OrderRequest."
            )

        payload: dict[str, Any] = {
            "tradingsymbol": request.instrument.symbol,
            "exchange": request.instrument.exchange,
            "transaction_type": (
                TransactionMapper.to_kite(
                    request.transaction_type,
                )
            ),
            "quantity": request.quantity,
            "product": ProductMapper.to_kite(
                request.product_type,
            ),
            "order_type": OrderTypeMapper.to_kite(
                request.order_type,
            ),
        }

        if request.price is not None:
            payload["price"] = request.price

        if request.trigger_price is not None:
            payload["trigger_price"] = (
                request.trigger_price
            )

        return payload