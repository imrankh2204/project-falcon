"""
Live trading orchestration service.

Coordinates live trade execution while remaining independent of any
specific broker implementation.

Responsibilities
----------------
- Coordinate live order execution.
- Invoke risk validation.
- Submit orders through BrokerGateway.
- Convert broker responses into ExecutionResult.
- Synchronize the portfolio.

The service intentionally does NOT implement:

- Strategy logic
- Broker SDK communication
- Authentication
- Portfolio persistence
"""

from __future__ import annotations

from app.live.broker_gateway import (
    BrokerGateway,
)
from app.live.execution_result import (
    ExecutionResult,
)
from app.live.order_request import (
    OrderRequest,
)
from app.portfolio.synchronization_service import (
    PortfolioSynchronizationService,
)
from app.trading.risk_manager import (
    RiskManager,
)
from app.broker.broker_account_facade import (
    BrokerAccountFacade,
)


class LiveTradingService:
    """
    Coordinates live trading operations.
    """

    def __init__(
        self,
        *,
        broker_gateway: BrokerGateway,
        account_facade: BrokerAccountFacade,
        risk_manager: RiskManager,
        synchronization_service: PortfolioSynchronizationService,
    ) -> None:
        """
        Initialize the live trading service.
        """

        if not isinstance(
            broker_gateway,
            BrokerGateway,
        ):
            raise TypeError(
                "broker_gateway must be a BrokerGateway."
            )

        if not isinstance(
            account_facade,
            BrokerAccountFacade,
        ):
            raise TypeError(
                "account_facade must be a BrokerAccountFacade."
            )

        if not isinstance(
            risk_manager,
            RiskManager,
        ):
            raise TypeError(
                "risk_manager must be a RiskManager."
            )

        if not isinstance(
            synchronization_service,
            PortfolioSynchronizationService,
        ):
            raise TypeError(
                "synchronization_service must be a "
                "PortfolioSynchronizationService."
            )

        self._broker_gateway = broker_gateway

        self._account_facade = account_facade

        self._risk_manager = risk_manager

        self._synchronization_service = (
            synchronization_service
        )

    def execute(
        self,
        order_request: OrderRequest,
    ) -> ExecutionResult:
        """
        Execute a live order.

        Workflow:

        1. Validate order risk.
        2. Submit order through broker gateway.
        3. Synchronize portfolio state.
        4. Return immutable execution result.

        Returns
        -------
        ExecutionResult
            Immutable broker execution result.
        """

        if not isinstance(
            order_request,
            OrderRequest,
        ):
            raise TypeError(
                "order_request must be an OrderRequest."
            )

        #
        # Retrieve the latest broker account snapshot.
        #
        snapshot = self._account_facade.get_snapshot()

        #
        # Defensive account validation.
        #
        if snapshot.profile is None:
            raise RuntimeError(
                "Broker account profile is unavailable."
            )

        if snapshot.margin is None:
            raise RuntimeError(
                "Broker account margin is unavailable."
            )
        
        #
        # Validate the order.
        #
        approved = self._risk_manager.approve(
            order_request,
            open_positions=[],
            trades_today=0,
        )

        if not approved:
            raise RuntimeError(
                "Order rejected by RiskManager."
            )

        #
        # Submit to broker.
        #
        order = self._broker_gateway.place_order(
            order_request,
        )

        #
        # Refresh portfolio snapshot.
        #
        self._synchronization_service.synchronize()

        #
        # Convert broker response into domain result.
        #
        return ExecutionResult(
            order=order,
            accepted=True,
            message="Order executed successfully.",
        )