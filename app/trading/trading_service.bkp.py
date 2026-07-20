"""
Application service for orchestrating trade execution.

The TradingService coordinates the trading workflow between the
strategy layer and the trading domain while keeping business rules
inside the appropriate domain components.

Responsibilities:
    * Coordinate trade approval.
    * Execute approved trades.
    * Register positions with the portfolio.

The TradingService intentionally owns no business rules.
"""

from __future__ import annotations

from app.trading.execution import PaperExecutionEngine
from app.trading.portfolio import Portfolio
from app.trading.position import Position
from app.trading.risk_manager import RiskManager
from app.trading.trade_request import TradeRequest


class TradingService:
    """
    Application service coordinating the trade workflow.
    """

    def __init__(
        self,
        risk_manager: RiskManager,
        execution_engine: PaperExecutionEngine,
        portfolio: Portfolio,
    ) -> None:
        """
        Initialize the trading service.

        Args:
            risk_manager:
                Domain risk manager.

            execution_engine:
                Paper execution engine.

            portfolio:
                Portfolio aggregate root.
        """

        self._risk_manager = risk_manager
        self._execution_engine = execution_engine
        self._portfolio = portfolio

    @property
    def portfolio(self) -> Portfolio:
        """
        Return the managed portfolio.
        """

        return self._portfolio

    def submit_trade(
        self,
        trade: TradeRequest,
        *,
        execution_price: float,
        trades_today: int,
    ) -> Position:
        """
        Submit a trade for execution.

        Workflow:

        1. Gather currently open positions.
        2. Perform risk approval.
        3. Execute the trade.
        4. Register the resulting position.
        5. Return the created position.

        Args:
            trade:
                Requested trade.

            execution_price:
                Paper execution price.

            trades_today:
                Number of completed trades today.

        Returns:
            Newly created Position.

        Raises:
            ValueError:
                If risk approval fails.

            Any exception raised by Portfolio or
            PaperExecutionEngine is intentionally propagated.
        """

        open_positions = [
            position
            for position in self._portfolio.positions.values()
            if position.is_open
        ]

        approved = self._risk_manager.approve(
            trade,
            open_positions=open_positions,
            trades_today=trades_today,
        )

        if not approved:
            raise ValueError("Trade request rejected by RiskManager.")
        position = self._execution_engine.execute(
            trade,
            execution_price=execution_price,
        )

        self._portfolio.add_position(position)

        return position