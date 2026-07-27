"""
Immutable live order model for Project Falcon.

Represents a broker-independent order accepted by a broker.

Responsibilities
----------------
- Store immutable order information.
- Remain broker independent.
- Provide deterministic transport semantics.

The model intentionally does NOT implement:

- Order placement
- Order modification
- Order cancellation
- Broker communication
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.live.order_id import OrderId
from app.live.order_status import OrderStatus
from app.live.order_type import OrderType
from app.live.product_type import ProductType
from app.live.transaction_type import TransactionType
from app.market.instrument import Instrument


@dataclass(frozen=True, slots=True)
class Order:
    """
    Immutable broker-independent order.
    """

    order_id: OrderId

    instrument: Instrument

    transaction_type: TransactionType

    order_type: OrderType

    product_type: ProductType

    status: OrderStatus

    quantity: int

    filled_quantity: int

    average_price: float

    price: float | None

    trigger_price: float | None

    created_at: datetime

    updated_at: datetime

    def __post_init__(self) -> None:
        """
        Validate the order.
        """

        if not isinstance(
            self.order_id,
            OrderId,
        ):
            raise TypeError(
                "order_id must be an OrderId."
            )

        if not isinstance(
            self.instrument,
            Instrument,
        ):
            raise TypeError(
                "instrument must be an Instrument."
            )

        if not isinstance(
            self.transaction_type,
            TransactionType,
        ):
            raise TypeError(
                "transaction_type must be a TransactionType."
            )

        if not isinstance(
            self.order_type,
            OrderType,
        ):
            raise TypeError(
                "order_type must be an OrderType."
            )

        if not isinstance(
            self.product_type,
            ProductType,
        ):
            raise TypeError(
                "product_type must be a ProductType."
            )

        if not isinstance(
            self.status,
            OrderStatus,
        ):
            raise TypeError(
                "status must be an OrderStatus."
            )

        if not isinstance(
            self.quantity,
            int,
        ):
            raise TypeError(
                "quantity must be an integer."
            )

        if not isinstance(
            self.filled_quantity,
            int,
        ):
            raise TypeError(
                "filled_quantity must be an integer."
            )

        if self.quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero."
            )

        if self.filled_quantity < 0:
            raise ValueError(
                "filled_quantity cannot be negative."
            )

        if self.filled_quantity > self.quantity:
            raise ValueError(
                "filled_quantity cannot exceed quantity."
            )

        if self.average_price < 0:
            raise ValueError(
                "average_price cannot be negative."
            )

        if (
            self.price is not None
            and self.price <= 0
        ):
            raise ValueError(
                "price must be greater than zero."
            )

        if (
            self.trigger_price is not None
            and self.trigger_price <= 0
        ):
            raise ValueError(
                "trigger_price must be greater than zero."
            )

        if not isinstance(
            self.created_at,
            datetime,
        ):
            raise TypeError(
                "created_at must be a datetime."
            )

        if not isinstance(
            self.updated_at,
            datetime,
        ):
            raise TypeError(
                "updated_at must be a datetime."
            )