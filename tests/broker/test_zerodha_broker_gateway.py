"""
Integration-style tests for the Zerodha broker gateway order flow.
"""

from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

from app.broker.zerodha.zerodha_broker_gateway import ZerodhaBrokerGateway
from app.live.order_request import OrderRequest
from app.live.order_type import OrderType
from app.live.product_type import ProductType
from app.live.transaction_type import TransactionType
from app.market.instrument import Instrument


def test_place_order_uses_mapper_and_returns_order() -> None:
    """
    Place order should map the request into Kite payload and return a domain Order.
    """

    instrument = Instrument(
        symbol="NIFTY 50",
        exchange="NSE",
        instrument_token=256265,
        lot_size=50,
        tick_size=0.05,
    )

    request = OrderRequest(
        instrument=instrument,
        transaction_type=TransactionType.BUY,
        quantity=100,
        order_type=OrderType.MARKET,
        product_type=ProductType.MIS,
    )

    gateway = ZerodhaBrokerGateway.__new__(ZerodhaBrokerGateway)
    gateway._kite = MagicMock()
    gateway._kite.place_order.return_value = "broker-order-1"
    gateway._kite.order_history.return_value = [
        {
            "order_id": "broker-order-1",
            "tradingsymbol": "NIFTY 50",
            "exchange": "NSE",
            "instrument_token": 256265,
            "transaction_type": "BUY",
            "quantity": 100,
            "product": "MIS",
            "order_type": "MARKET",
            "status": "COMPLETE",
            "filled_quantity": 100,
            "average_price": 250.0,
            "price": None,
            "trigger_price": None,
            "order_timestamp": datetime.now().isoformat(),
            "exchange_update_timestamp": datetime.now().isoformat(),
        }
    ]
    gateway._session_manager = MagicMock()
    gateway._session_manager.session = None
    gateway._execute = MagicMock(side_effect=lambda fn: fn())

    order = gateway.place_order(request)

    gateway._kite.place_order.assert_called_once()
    assert order.order_id.value == "broker-order-1"
    assert order.quantity == 100
