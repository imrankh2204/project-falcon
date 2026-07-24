"""
Application service for orchestrating trade execution.

The TradingService coordinates the trading workflow between the
strategy layer and the trading domain while keeping business rules
inside the appropriate domain components.

Responsibilities:
    * Coordinate trade approval.
    * Execute approved trades.
    * Coordinate position exits.
    * Register positions with the portfolio.

The TradingService intentionally owns no business rules.
"""

from __future__ import annotations

from datetime import datetime

from app.market.instrument import Instrument
from app.trading.execution import PaperExecutionEngine
from app.trading.portfolio import Portfolio
from app.trading.position import Position
from app.trading.risk_manager import RiskManager
from app.trading.trade_request import TradeRequest


class TradingService:
    """
    Application service coordinating the trading workflow.
    """

    def __init__(
        self,
        risk_manager: RiskManager,
        execution_engine: PaperExecutionEngine,
        portfolio: Portfolio,
    ) -> None:
        """
        Initialize the trading service.
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

        Workflow

        1. Gather currently open positions.
        2. Perform risk approval.
        3. Execute the trade.
        4. Register the resulting position.
        5. Return the created position.

        Raises
        ------
        ValueError
            If risk approval fails.

        Any domain exception is intentionally propagated unchanged.
        """

        approved = self._risk_manager.approve(
            trade,
            open_positions=self._portfolio.get_open_positions(),
            trades_today=trades_today,
        )

        if not approved:
            raise ValueError(
                "Trade request rejected by RiskManager."
            )

        position = self._execution_engine.execute(
            trade,
            execution_price=execution_price,
        )

        self._portfolio.add_position(position)

        return position

    def close_open_position(
        self,
        *,
        instrument: Instrument,
        exit_price: float,
        exit_time: datetime,
    ) -> Position:
        """
        Close the currently open position for the supplied instrument.

        Parameters
        ----------
        instrument
            Instrument whose open position should be closed.

        exit_price
            Exit execution price.

        exit_time
            Exit timestamp.

        Returns
        -------
        Position
            The closed position.

        Raises
        ------
        ValueError
            If no open position exists or the instrument does not
            match the current open position.

        Any Position lifecycle exception is propagated unchanged.
        """

        position = self._portfolio.get_open_position()

        if position is None:
            raise ValueError(
                "No open position exists."
            )

        if position.instrument != instrument:
            raise ValueError(
                "Open position instrument does not match."
            )

        position.close(
            exit_price=exit_price,
            exit_time=exit_time,
        )

        return position

    def close_all_open_positions(
        self,
        *,
        exit_price: float,
        exit_time: datetime,
    ) -> tuple[Position, ...]:
        """
        Close every currently open position.

        Returns
        -------
        tuple[Position, ...]
            Immutable collection of closed positions.

        Notes
        -----
        Under the current Falcon architecture this collection
        contains either zero or one position. The API remains
        future-compatible with multi-position portfolios.
        """

        closed_positions: list[Position] = []

        for position in self._portfolio.get_open_positions():
            position.close(
                exit_price=exit_price,
                exit_time=exit_time,
            )

            closed_positions.append(position)

        return tuple(closed_positions)