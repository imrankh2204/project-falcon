from __future__ import annotations

from app.live.order_request import OrderRequest
from app.trading.risk_manager import RiskManager


class LiveRiskValidator:
    """
    Adapts the trading RiskManager for live order validation.
    """

    def __init__(self, risk_manager: RiskManager) -> None:
        self._risk_manager = risk_manager

    def validate(self, order_request: OrderRequest) -> bool:
        """
        Validate a live order request.

        The first implementation is intentionally permissive until
        live portfolio state is integrated.
        """

        return True