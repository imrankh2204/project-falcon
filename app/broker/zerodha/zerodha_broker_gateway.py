"""
Concrete Zerodha BrokerGateway implementation.

This module adapts Kite Connect to Falcon's broker-independent live
trading contracts.

Responsibilities
----------------
- Retrieve live quotes.
- Retrieve broker positions.
- Place orders.
- Cancel orders.
- Retrieve order status.
- Translate Kite exceptions into Falcon exceptions.

The gateway intentionally does NOT implement:

- Authentication
- Session lifecycle management
- Risk management
- Trading logic
- Retry logic
- Market data caching
"""

from __future__ import annotations

from typing import Any
from typing import Callable
from typing import TypeVar

from kiteconnect import KiteConnect

from app.broker.zerodha.exception_mapper import (
    ExceptionMapper,
)
from app.broker.zerodha.session_manager import (
    SessionManager,
)
from app.broker.zerodha.order_response_mapper import (
    OrderResponseMapper,
)
from app.broker.broker_session_recovery_service import (
    BrokerSessionRecoveryService,
)
from app.broker.idempotent_order_executor import (
    IdempotentOrderExecutor,
)
from app.live.broker_session import (
    BrokerSession,
)
from app.live.broker_gateway import (
    BrokerGateway,
)
from app.live.broker_position import (
    BrokerPosition,
)
from app.broker.zerodha.order_mapper import (
    OrderMapper,
)
from app.live.exceptions import (
    SessionExpiredError,
)
from app.live.order import (
    Order,
)
from app.live.order_id import (
    OrderId,
)
from app.live.order_request import (
    OrderRequest,
)
from app.live.order_status import (
    OrderStatus,
)
from app.live.quote import (
    Quote,
)
from app.market.instrument import (
    Instrument,
)


T = TypeVar("T")


class ZerodhaBrokerGateway(BrokerGateway):
    """
    Concrete BrokerGateway backed by Kite Connect.

    This adapter is responsible only for translating between Falcon
    domain objects and the Kite Connect SDK.
    """

    def __init__(
        self,
        session_manager: SessionManager,
    ) -> None:
        """
        Initialize the gateway using the SessionManager.
        """

        if not isinstance(
            session_manager,
            SessionManager,
        ):
            raise TypeError(
                "session_manager must be a SessionManager."
            )

        self._session_manager = session_manager

        self._kite: KiteConnect = self._session_manager.kite

        self._recovery_service = (
            BrokerSessionRecoveryService(
                recovery_callback=self._recover_session,
            )
        )

        self._order_executor = (
            IdempotentOrderExecutor()
        )

    #
    # Internal helpers
    #

    def _execute(
        self,
        operation: Callable[[], T],
    ) -> T:
        """
        Execute Kite operation and translate exceptions.
        """

        try:
            return self._recovery_service.execute(
            operation,
        )

        except Exception as exc:
            raise ExceptionMapper.translate(
                exc,
            ) from exc

    def _recover_session(self) -> None:
        """
        Recover the current broker session.

        The recovery logic is intentionally delegated to the
        SessionManager so that the gateway remains broker-neutral.
        """

        self._session_manager.authenticate()

        self._kite = self._session_manager.kite

    def _instrument_key(
        self,
        instrument: Instrument,
    ) -> str:
        """
        Convert Falcon Instrument into Kite quote key.
        """

        if not isinstance(
            instrument,
            Instrument,
        ):
            raise TypeError(
                "instrument must be an Instrument."
            )

        return (
            f"{instrument.exchange}:"
            f"{instrument.symbol}"
        )

    def _map_quote(
        self,
        instrument: Instrument,
        data: dict[str, Any],
    ) -> Quote:
        """
        Convert Kite quote payload into Falcon Quote.
        """

        if not isinstance(
            data,
            dict,
        ):
            raise TypeError(
                "data must be a dictionary."
            )

        depth = data.get(
            "depth",
            {},
        )

        buy = depth.get(
            "buy",
            [],
        )

        sell = depth.get(
            "sell",
            [],
        )

        bid = 0.0

        ask = 0.0

        if buy:
            bid = float(
                buy[0].get(
                    "price",
                    0.0,
                )
            )

        if sell:
            ask = float(
                sell[0].get(
                    "price",
                    0.0,
                )
            )

        return Quote(
            instrument=instrument,
            last_price=float(
                data.get(
                    "last_price",
                    0.0,
                )
            ),
            bid=bid,
            ask=ask,
            volume=float(
                data.get(
                    "volume",
                    0.0,
                )
            ),
            timestamp=data.get(
                "timestamp",
            ),
        )

    #
    # BrokerGateway implementation
    #

    def quote(
        self,
        instrument: Instrument,
    ) -> Quote:
        """
        Retrieve a single live quote.
        """

        key = self._instrument_key(
            instrument
        )

        response = self._execute(
            lambda: self._kite.quote(
                key
            )
        )

        payload = response.get(
            key
        )

        if payload is None:
            raise ValueError(
                f"No quote returned for {key}."
            )

        return self._map_quote(
            instrument,
            payload,
        )

    def quotes(
        self,
        instruments: tuple[
            Instrument,
            ...,
        ],
    ) -> tuple[
        Quote,
        ...,
    ]:
        """
        Retrieve multiple live quotes.
        """

        if not isinstance(
            instruments,
            tuple,
        ):
            raise TypeError(
                "instruments must be a tuple."
            )

        keys = tuple(
            self._instrument_key(
                instrument
            )
            for instrument in instruments
        )

        if not keys:
            return ()

        response = self._execute(
            lambda: self._kite.quote(
                keys
            )
        )

        quotes: list[Quote] = []

        for instrument in instruments:
            key = self._instrument_key(
                instrument
            )

            payload = response.get(
                key
            )

            if payload is None:
                raise ValueError(
                    f"No quote returned for {key}."
                )

            quotes.append(
                self._map_quote(
                    instrument,
                    payload,
                )
            )

        return tuple(
            quotes
        )

    def authenticate(
        self,
    ) -> BrokerSession:
        """
        Implemented by session management layer.
        """

        return self._session_manager.authenticate()

    def session(
        self,
    ) -> BrokerSession | None:
        """
        Return active session.
        """

        return self._session_manager.session

    def logout(
        self,
    ) -> None:
        """
        Logout is managed by session manager.
        """

        self._session_manager.logout()

    def place_order(
        self,
        request: OrderRequest,
    ) -> Order:
        """
        Submit a live order through Kite Connect.

        Parameters
        ----------
        request
            Broker-independent order request.

        Returns
        -------
        Order
            Broker-acknowledged immutable order.
        """

        if not isinstance(
            request,
            OrderRequest,
        ):
            raise TypeError(
                "request must be an OrderRequest."
            )

        payload = OrderMapper.to_kite(
            request,
        )

        key = (
            f"{request.instrument.exchange}:"
            f"{request.instrument.symbol}:"
            f"{request.transaction_type.name}:"
            f"{request.quantity}"
        )

        try:
            broker_order_id = self._order_executor.execute(
                key=key,
                operation=lambda: self._execute(
                    lambda: self._kite.place_order(
                        **payload,
                    )
                ),
            )

        except SessionExpiredError:
            self._recovery_service.recover()

            broker_order_id = self._order_executor.execute(
                key=key,
                operation=lambda: self._execute(
                    lambda: self._kite.place_order(
                        **payload,
                    )
                ),
            )

        return self.get_order(
            OrderId(
                broker_order_id,
            )
        )

    def cancel_order(
        self,
        order_id: OrderId,
    ):
        """
        Cancel an existing broker order.
        """

        if not isinstance(
            order_id,
            OrderId,
        ):
            raise TypeError(
                "order_id must be an OrderId."
            )

        self._execute(
            lambda: self._kite.cancel_order(
                order_id=str(
                    order_id,
                ),
            )
        )

    def get_order(
        self,
        order_id: OrderId,
    ) -> Order:
        """
        Retrieve an order from Kite Connect.
        """

        if not isinstance(
            order_id,
            OrderId,
        ):
            raise TypeError(
                "order_id must be an OrderId."
            )

        history = self._execute(
            lambda: self._kite.order_history(
                order_id=str(
                    order_id,
                ),
            )
        )

        if not history:
            raise ValueError(
                f"No order found for {order_id}."
            )

        payload = history[-1]

        instrument = Instrument(
            exchange=payload["exchange"],
            symbol=payload["tradingsymbol"],
            instrument_token=int(
                payload["instrument_token"],
            ),
            lot_size=1,
            tick_size=0.05,
            expiry=None,
            strike=None,
            option_type=None,
        )

        return OrderResponseMapper.from_kite(
            instrument=instrument,
            payload=payload,
        )

    def orders(
        self,
    ) -> tuple[Order, ...]:
        """
        Retrieve all broker orders.
        """


        payloads = self._execute(
            lambda: self._kite.orders()
        )

        orders: list[Order] = []

        for payload in payloads:

            instrument = Instrument(
                exchange=payload["exchange"],
                symbol=payload["tradingsymbol"],
                instrument_token=int(
                    payload["instrument_token"],
                ),
                lot_size=1,
                tick_size=0.05,
                expiry=None,
                strike=None,
                option_type=None,
            )

            orders.append(
                OrderResponseMapper.from_kite(
                    instrument=instrument,
                    payload=payload,
                )
            )

        return tuple(
            orders,
        )

    def positions(
        self,
    ) -> tuple[BrokerPosition, ...]:
        """
        Retrieve all broker positions.
        """

        response = self._execute(
            lambda: self._kite.positions()
        )

        payloads = response.get(
            "net",
            [],
        )

        positions: list[BrokerPosition] = []

        for payload in payloads:

            instrument = Instrument(
                exchange=payload["exchange"],
                symbol=payload["tradingsymbol"],
                instrument_token=int(
                    payload["instrument_token"],
                ),
                lot_size=1,
                tick_size=0.05,
                expiry=None,
                strike=None,
                option_type=None,
            )

            positions.append(
                PositionResponseMapper.from_kite(
                    instrument=instrument,
                    payload=payload,
                )
            )

        return tuple(
            positions,
        )