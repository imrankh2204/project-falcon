"""
Maps Kite order payloads into Falcon Order objects.

Responsibilities
----------------
- Translate Kite order responses.
- Produce immutable Falcon Order objects.
- Normalize broker values into Falcon enums.

The mapper intentionally does NOT implement:

- Broker communication
- Order placement
- Order cancellation
- SDK lifecycle
"""

from __future__ import annotations

from datetime import datetime

from app.live.order import (
    Order,
)
from app.live.order_id import (
    OrderId,
)
from app.live.order_status import (
    OrderStatus,
)
from app.live.order_type import (
    OrderType,
)
from app.live.product_type import (
    ProductType,
)
from app.live.transaction_type import (
    TransactionType,
)
from app.market.instrument import (
    Instrument,
)


class OrderResponseMapper:
    """
    Maps Kite order payloads into Falcon Order objects.
    """

    @classmethod
    def from_kite(
        cls,
        instrument: Instrument,
        payload: dict,
    ) -> Order:
        """
        Convert a Kite order payload into a Falcon Order.
        """

        if not isinstance(
            instrument,
            Instrument,
        ):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(
            payload,
            dict,
        ):
            raise TypeError(
                "payload must be a dictionary."
            )

        return Order(
            order_id=OrderId(
                payload["order_id"],
            ),
            instrument=instrument,
            transaction_type=cls._transaction_type(
                payload["transaction_type"],
            ),
            order_type=cls._order_type(
                payload["order_type"],
            ),
            product_type=cls._product_type(
                payload["product"],
            ),
            status=cls._status(
                payload["status"],
            ),
            quantity=int(
                payload["quantity"],
            ),
            filled_quantity=int(
                payload.get(
                    "filled_quantity",
                    0,
                )
            ),
            average_price=float(
                payload.get(
                    "average_price",
                    0.0,
                )
            ),
            price=(
                float(payload["price"])
                if payload.get("price")
                is not None
                else None
            ),
            trigger_price=(
                float(
                    payload["trigger_price"]
                )
                if payload.get(
                    "trigger_price"
                )
                is not None
                else None
            ),
            created_at=cls._datetime(
                payload["order_timestamp"],
            ),
            updated_at=cls._datetime(
                payload.get(
                    "exchange_update_timestamp",
                    payload["order_timestamp"],
                )
            ),
        )

    @staticmethod
    def _datetime(
        value: str | datetime,
    ) -> datetime:
        """
        Normalize Kite timestamps.
        """

        if isinstance(
            value,
            datetime,
        ):
            return value

        return datetime.fromisoformat(
            value,
        )

    @staticmethod
    def _transaction_type(
        value: str,
    ) -> TransactionType:

        return TransactionType(
            value.upper(),
        )

    @staticmethod
    def _order_type(
        value: str,
    ) -> OrderType:

        value = value.upper()

        if value == "SL-M":
            value = "SL_MARKET"

        return OrderType(
            value,
        )

    @staticmethod
    def _product_type(
        value: str,
    ) -> ProductType:

        return ProductType(
            value.upper(),
        )

    @staticmethod
    def _status(
        value: str,
    ) -> OrderStatus:

        mapping = {
            "OPEN": OrderStatus.OPEN,
            "COMPLETE": OrderStatus.FILLED,
            "CANCELLED": OrderStatus.CANCELLED,
            "REJECTED": OrderStatus.REJECTED,
            "TRIGGER PENDING": OrderStatus.OPEN,
            "VALIDATION PENDING": OrderStatus.NEW,
            "PUT ORDER REQ RECEIVED": OrderStatus.NEW,
        }

        try:
            return mapping[
                value.upper()
            ]

        except KeyError as exc:
            raise ValueError(
                f"Unsupported order status: {value}"
            ) from exc