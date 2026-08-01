"""
Portfolio synchronization service.

Coordinates synchronization between the broker layer and Falcon's
portfolio domain.

Responsibilities
----------------
- Retrieve broker positions.
- Convert broker positions into portfolio positions.
- Provide synchronization entry points.
- Remain broker independent.

The service intentionally does NOT implement:

- Position reconciliation
- Portfolio mutation
- P&L calculations
- Risk management
"""

from __future__ import annotations

from app.live.broker_gateway import (
    BrokerGateway,
)
from app.live.broker_position import (
    BrokerPosition,
)
from app.portfolio.portfolio_position import (
    PortfolioPosition,
)
from app.portfolio.portfolio import (
    Portfolio,
)

class PortfolioSynchronizationService:
    """
    Coordinates portfolio synchronization.
    """

    def __init__(
        self,
        *,
        broker_gateway: BrokerGateway,
    ) -> None:
        """
        Initialize the synchronization service.
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

    def broker_positions(
        self,
    ) -> tuple[
        BrokerPosition,
        ...,
    ]:
        """
        Retrieve broker positions.
        """

        return self._broker_gateway.positions()

    def _to_portfolio_position(
        self,
        broker_position: BrokerPosition,
    ) -> PortfolioPosition:
        """
        Convert a broker position into a portfolio position.
        """

        if not isinstance(
            broker_position,
            BrokerPosition,
        ):
            raise TypeError(
                "broker_position must be a BrokerPosition."
            )

        return PortfolioPosition(
            instrument=broker_position.instrument,
            quantity=broker_position.quantity,
            average_price=broker_position.average_price,
            realized_pnl=broker_position.realized_pnl,
            unrealized_pnl=broker_position.unrealized_pnl,
        )

    def _reconcile(
        self,
        *,
        existing: Portfolio,
        latest: Portfolio,
    ) -> Portfolio:
        """
        Reconcile an existing portfolio with the latest broker snapshot.
        """

        if not isinstance(
            existing,
            Portfolio,
        ):
            raise TypeError(
                "existing must be a Portfolio."
            )

        if not isinstance(
            latest,
            Portfolio,
        ):
            raise TypeError(
                "latest must be a Portfolio."
            )

        latest_by_instrument = {
            position.instrument: position
            for position in latest.positions
        }

        reconciled = []

        for position in latest.positions:
            reconciled.append(
                latest_by_instrument[position.instrument]
            )

        return Portfolio(
            positions=tuple(reconciled),
        )

    def synchronize(
        self,
        *,
        existing_portfolio: Portfolio | None = None,
    ) -> Portfolio:
        """
        Synchronize the portfolio from the broker.

        Parameters
        ----------
        existing_portfolio
            Existing immutable portfolio snapshot.

        Returns
        -------
        Portfolio
            Latest immutable portfolio snapshot.
        """

        latest = Portfolio(
            positions=tuple(
                self._to_portfolio_position(
                    broker_position,
                )
                for broker_position
                in self.broker_positions()
            ),
        )

        if existing_portfolio is None:
            return latest

        return self._reconcile(
            existing=existing_portfolio,
            latest=latest,
        )