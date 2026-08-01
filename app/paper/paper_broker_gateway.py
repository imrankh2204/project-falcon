"""
In-memory paper broker gateway for Project Falcon.

Implements the BrokerGateway contract without requiring any external
broker SDK or network connectivity.

Responsibilities
----------------
- Simulate broker authentication.
- Execute paper orders immediately.
- Maintain in-memory order state.
- Maintain in-memory position state.
- Provide deterministic market quotes.

The implementation intentionally does NOT provide:

- Network communication
- Persistent storage
- Real broker connectivity
- Slippage simulation
- Partial fills
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict

from app.live.broker_gateway import BrokerGateway
from app.live.broker_position import BrokerPosition
from app.live.broker_session import BrokerSession
from app.live.exceptions import (
    AuthenticationError,
    OrderNotFoundError,
    OrderRejectedError,
)
from app.live.order import Order
from app.live.order_id import OrderId
from app.live.order_request import OrderRequest
from app.live.order_status import OrderStatus
from app.live.quote import Quote
from app.market.instrument import Instrument


class PaperBrokerGateway(BrokerGateway):
    """
    Deterministic in-memory broker implementation.

    Every accepted order is immediately filled.
    """

    def __init__(self) -> None:

        self._session: BrokerSession | None = None

        self._orders: Dict[
            str,
            Order,
        ] = {}

        self._positions: Dict[
            str,
            BrokerPosition,
        ] = {}

        self._quotes: Dict[
            str,
            Quote,
        ] = {}

        self._next_order_number = 1

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _require_session(self) -> BrokerSession:
        """
        Ensure an authenticated session exists.
        """

        if self._session is None:
            raise AuthenticationError(
                "Broker session has not been established."
            )

        if self._session.is_expired:
            raise AuthenticationError(
                "Broker session has expired."
            )

        return self._session

    def _next_order_id(self) -> OrderId:
        """
        Generate the next deterministic paper order id.
        """

        order_id = OrderId(
            f"PAPER-{self._next_order_number:06d}"
        )

        self._next_order_number += 1

        return order_id

    # ---------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------

    def authenticate(
        self,
    ) -> BrokerSession:
        """
        Create an authenticated paper session.
        """

        now = datetime.now()

        self._session = BrokerSession(
            broker_name="PaperBroker",
            user_id="paper-user",
            access_token="paper-session",
            authenticated_at=now,
            expires_at=None,
        )

        return self._session

    def session(
        self,
    ) -> BrokerSession | None:
        """
        Return the active paper session.
        """

        return self._session

    def logout(
        self,
    ) -> None:
        """
        Terminate the current paper session.
        """

        self._session = None

    # ---------------------------------------------------------
    # Order Management
    # ---------------------------------------------------------

    def place_order(
        self,
        order_request: OrderRequest,
    ) -> Order:
        """
        Submit a paper order.

        Paper execution is deterministic:

        - immediate fill
        - full quantity executed
        - average price derived from the latest quote if available
        """

        self._require_session()

        if not isinstance(
            order_request,
            OrderRequest,
        ):
            raise TypeError(
                "order_request must be an OrderRequest."
            )

        now = datetime.now()

        #
        # Determine execution price.
        #
        quote = self._quotes.get(
            order_request.instrument.symbol,
        )

        if quote is None:
            raise OrderRejectedError(
                f"No quote available for "
                f"{order_request.instrument.symbol}."
            )

        execution_price = quote.last_price

        order = Order(
            order_id=self._next_order_id(),
            instrument=order_request.instrument,
            transaction_type=(
                order_request.transaction_type
            ),
            order_type=order_request.order_type,
            product_type=order_request.product_type,
            status=OrderStatus.FILLED,
            quantity=order_request.quantity,
            filled_quantity=order_request.quantity,
            average_price=execution_price,
            price=execution_price,
            trigger_price=None,
            created_at=now,
            updated_at=now,
        )

        self._orders[
            order.order_id.value
        ] = order

        #
        # Update in-memory position snapshot.
        #
        self._positions[
            order.instrument.symbol
        ] = BrokerPosition(
            instrument=order.instrument,
            quantity=order.quantity,
            average_price=execution_price,
            realized_pnl=0.0,
            unrealized_pnl=0.0,
        )

        return order

    def cancel_order(
        self,
        order_id: OrderId,
    ) -> Order:
        """
        Cancel an existing paper order.
        """

        self._require_session()

        if not isinstance(
            order_id,
            OrderId,
        ):
            raise TypeError(
                "order_id must be an OrderId."
            )

        order = self._orders.get(
            order_id.value,
        )

        if order is None:
            raise OrderNotFoundError(
                f"Unknown order '{order_id}'."
            )

        #
        # Filled paper orders cannot be cancelled.
        #
        return order

    def get_order(
        self,
        order_id: OrderId,
    ) -> Order:
        """
        Retrieve a paper order.
        """

        self._require_session()

        if not isinstance(
            order_id,
            OrderId,
        ):
            raise TypeError(
                "order_id must be an OrderId."
            )

        order = self._orders.get(
            order_id.value,
        )

        if order is None:
            raise OrderNotFoundError(
                f"Unknown order '{order_id}'."
            )

        return order

    def orders(
        self,
    ) -> tuple[Order, ...]:
        """
        Return all paper orders.
        """

        self._require_session()

        return tuple(
            self._orders.values()
        )

    # ---------------------------------------------------------
    # Position Management
    # ---------------------------------------------------------

    def positions(
        self,
    ) -> tuple[BrokerPosition, ...]:
        """
        Return all paper positions.
        """

        self._require_session()

        return tuple(
            self._positions.values()
        )

    # ---------------------------------------------------------
    # Market Quotes
    # ---------------------------------------------------------

    def quote(
        self,
        instrument: Instrument,
    ) -> Quote:
        """
        Return the latest paper quote.
        """

        self._require_session()

        if not isinstance(
            instrument,
            Instrument,
        ):
            raise TypeError(
                "instrument must be an Instrument."
            )

        quote = self._quotes.get(
            instrument.symbol,
        )

        if quote is None:
            raise OrderNotFoundError(
                f"No quote available for "
                f"{instrument.symbol}."
            )

        return quote

    # ---------------------------------------------------------
    # Paper-only helper methods
    # ---------------------------------------------------------

    def update_quote(
        self,
        quote: Quote,
    ) -> None:
        """
        Register or replace the latest paper quote.

        This helper is intended for paper trading,
        replay, and unit testing. It is not part of
        the BrokerGateway interface.
        """

        if not isinstance(
            quote,
            Quote,
        ):
            raise TypeError(
                "quote must be a Quote."
            )

        self._quotes[
            quote.instrument.symbol
        ] = quote