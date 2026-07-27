"""
Abstract broker gateway for Project Falcon.

Defines the broker-independent contract implemented by all live broker
integrations.

Responsibilities
----------------
- Authenticate with a broker.
- Manage broker sessions.
- Submit live orders.
- Cancel live orders.
- Retrieve orders.
- Retrieve positions.
- Retrieve market quotes.

The interface intentionally does NOT implement:

- Broker SDK integration
- Strategy execution
- Portfolio management
- Risk management
- Replay
- Reporting
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.live.broker_position import BrokerPosition
from app.live.broker_session import BrokerSession
from app.live.order import Order
from app.live.order_id import OrderId
from app.live.quote import Quote
from app.market.instrument import Instrument


class BrokerGateway(ABC):
    """
    Abstract broker gateway.

    Every live broker implementation must implement this interface.
    """

    @abstractmethod
    def authenticate(self) -> BrokerSession:
        """
        Authenticate with the broker.

        Returns
        -------
        BrokerSession
            Immutable authenticated broker session.
        """

    @abstractmethod
    def session(self) -> BrokerSession | None:
        """
        Return the current authenticated session.

        Returns
        -------
        BrokerSession | None
            Active session if authenticated.
        """

    @abstractmethod
    def logout(self) -> None:
        """
        Terminate the current broker session.
        """

    @abstractmethod
    def place_order(
        self,
        order: Order,
    ) -> Order:
        """
        Submit a live order.

        Parameters
        ----------
        order
            Immutable broker-independent order.

        Returns
        -------
        Order
            Broker-confirmed order.
        """

    @abstractmethod
    def cancel_order(
        self,
        order_id: OrderId,
    ) -> Order:
        """
        Cancel an existing order.

        Parameters
        ----------
        order_id
            Broker order identifier.

        Returns
        -------
        Order
            Updated cancelled order.
        """

    @abstractmethod
    def get_order(
        self,
        order_id: OrderId,
    ) -> Order:
        """
        Retrieve an order.

        Parameters
        ----------
        order_id
            Broker order identifier.

        Returns
        -------
        Order
            Current broker order state.
        """

    @abstractmethod
    def orders(self) -> tuple[Order, ...]:
        """
        Retrieve all known broker orders.

        Returns
        -------
        tuple[Order, ...]
            Immutable collection of broker orders.
        """

    @abstractmethod
    def positions(
        self,
    ) -> tuple[BrokerPosition, ...]:
        """
        Retrieve broker positions.

        Returns
        -------
        tuple[BrokerPosition, ...]
            Immutable collection of broker positions.
        """

    @abstractmethod
    def quote(
        self,
        instrument: Instrument,
    ) -> Quote:
        """
        Retrieve a live quote.

        Parameters
        ----------
        instrument
            Instrument being requested.

        Returns
        -------
        Quote
            Latest market quote.
        """