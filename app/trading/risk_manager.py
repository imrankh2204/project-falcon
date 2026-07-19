"""
Risk manager for Project Falcon.
"""

from __future__ import annotations

from app.trading.position import Position
from app.trading.trade_request import TradeRequest


class RiskManager:
    """
    Applies portfolio-level trading rules before execution.
    """

    def __init__(
        self,
        *,
        max_open_positions: int = 1,
        max_trades_per_day: int = 3,
    ) -> None:

        self._max_open_positions = max_open_positions
        self._max_trades_per_day = max_trades_per_day

    def approve(
        self,
        trade: TradeRequest,
        *,
        open_positions: list[Position],
        trades_today: int,
    ) -> bool:
        """
        Return True if the trade is permitted.
        """

        if trade.quantity <= 0:
            return False

        if len(open_positions) >= self._max_open_positions:
            return False

        if trades_today >= self._max_trades_per_day:
            return False

        return True