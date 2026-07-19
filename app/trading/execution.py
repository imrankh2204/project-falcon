"""
Paper execution engine for Project Falcon.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.trading.position import Position
from app.trading.trade_request import TradeRequest


class PaperExecutionEngine:
    """
    Executes approved trade requests in paper trading mode.

    This execution engine is intentionally broker-independent.
    It converts an approved TradeRequest into an active Position.

    Responsibilities:
        - Create Position objects.
        - Generate unique position identifiers.
        - Capture execution timestamp.
        - Populate entry price.
        - Return initialized Position.

    It is NOT responsible for:
        - Risk validation
        - Market data retrieval
        - Portfolio management
        - Broker communication
        - Order routing
    """

    def execute(
        self,
        request: TradeRequest,
        execution_price: float,
    ) -> Position:
        """
        Execute an approved trade request.

        Parameters
        ----------
        request:
            Approved trade request.

        execution_price:
            Price at which the order is assumed to have been filled.

        Returns
        -------
        Position
            Newly created open trading position.
        """

        return Position(
            position_id=str(uuid.uuid4()),
            instrument=request.instrument,
            signal=request.signal,
            quantity=request.quantity,
            entry_price=execution_price,
            entry_time=datetime.now(timezone.utc),
        )