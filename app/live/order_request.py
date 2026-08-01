"""
Immutable broker-independent order request model for Project Falcon.

Represents an executable order instruction after strategy intent has
been translated into live trading semantics.

Responsibilities
----------------
- Store normalized order details.
- Remain broker independent.
- Provide deterministic transport semantics.

The model intentionally does NOT implement:

- Broker communication
- Risk validation
- Order placement
- Portfolio synchronization
"""

from __future__ import annotations

from dataclasses import dataclass

from app.live.order_type import OrderType
from app.live.product_type import ProductType
from app.live.transaction_type import TransactionType
from app.market.instrument import Instrument


@dataclass(frozen=True, slots=True)
class OrderRequest:
    """
    Immutable broker-independent order request.
    """

    instrument: Instrument

    transaction_type: TransactionType

    quantity: int

    order_type: OrderType

    product_type: ProductType

    def __post_init__(self) -> None:
        """
        Validate order request fields.
        """

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
            self.quantity,
            int,
        ):
            raise TypeError(
                "quantity must be an integer."
            )

        if self.quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero."
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