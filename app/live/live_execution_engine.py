"""
Live execution bridge for Project Falcon.

Connects the trading domain request model with the live trading service.

Responsibilities
----------------
- Translate TradeRequest into OrderRequest.
- Delegate execution to LiveTradingService.
- Remain broker independent.

The engine intentionally does NOT implement:

- Broker communication
- Risk management
- Portfolio synchronization
- Strategy logic
"""

from __future__ import annotations

from app.live.live_trading_service import LiveTradingService
from app.live.execution_result import ExecutionResult
from app.live.order_request import OrderRequest
from app.live.order_type import OrderType
from app.live.product_type import ProductType
from app.live.transaction_type import TransactionType
from app.strategies.signal import Signal
from app.trading.trade_request import TradeRequest


class LiveExecutionEngine:
    """
    Converts trading intent into live execution requests.
    """

    def __init__(
        self,
        *,
        live_trading_service: LiveTradingService,
    ) -> None:
        """
        Initialize live execution engine.
        """

        if not isinstance(
            live_trading_service,
            LiveTradingService,
        ):
            raise TypeError(
                "live_trading_service must be a "
                "LiveTradingService."
            )

        self._live_trading_service = (
            live_trading_service
        )

    def execute(
        self,
        trade_request: TradeRequest,
    ) -> ExecutionResult:
        """
        Execute a trade request.

        TradeRequest belongs to the trading domain.
        OrderRequest belongs to the live domain.
        """

        if not isinstance(
            trade_request,
            TradeRequest,
        ):
            raise TypeError(
                "trade_request must be a TradeRequest."
            )

        order_request = (
            self._create_order_request(
                trade_request
            )
        )

        return self._live_trading_service.execute(
            order_request
        )

    def _create_order_request(
        self,
        trade_request: TradeRequest,
    ) -> OrderRequest:
        """
        Translate TradeRequest into OrderRequest.
        """

        transaction_type = (
            self._map_signal(
                trade_request.signal
            )
        )

        return OrderRequest(
            instrument=trade_request.instrument,
            transaction_type=transaction_type,
            quantity=trade_request.quantity,
            order_type=OrderType.MARKET,
            product_type=ProductType.MIS,
        )

    @staticmethod
    def _map_signal(
        signal: Signal,
    ) -> TransactionType:
        """
        Convert strategy signal into transaction type.
        """

        if signal == Signal.BUY:
            return TransactionType.BUY

        if signal == Signal.SELL:
            return TransactionType.SELL

        raise ValueError(
            "HOLD signal cannot create an order."
        )