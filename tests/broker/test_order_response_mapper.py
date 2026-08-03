"""
Unit tests for the Zerodha order response mapper.
"""

from __future__ import annotations

from datetime import datetime

from app.broker.zerodha.order_response_mapper import OrderResponseMapper
from app.live.order_status import OrderStatus
from app.live.order_type import OrderType
from app.live.product_type import ProductType
from app.live.transaction_type import TransactionType
from app.market.instrument import Instrument


def test_from_kite_maps_payload_to_domain_order() -> None:
    """
    Kite order payloads should be translated into a broker-neutral Order model.
    """

    instrument = Instrument(
        symbol="NIFTY 50",
        exchange="NSE",
        instrument_token=256265,
        lot_size=50,
        tick_size=0.05,
    )

    payload = {
        "order_id": "broker-order-1",
        "tradingsymbol": "NIFTY 50",
        "exchange": "NSE",
        "transaction_type": "BUY",
        "quantity": 100,
        "product": "MIS",
        "order_type": "MARKET",
        "status": "COMPLETE",
        "filled_quantity": 100,
        "average_price": 250.0,
        "price": 250.0,
        "trigger_price": None,
        "order_timestamp": "2024-01-01T10:00:00",
        "exchange_update_timestamp": "2024-01-01T10:05:00",
    }

    order = OrderResponseMapper.from_kite(instrument, payload)

    assert order.order_id.value == "broker-order-1"
    assert order.instrument == instrument
    assert order.transaction_type == TransactionType.BUY
    assert order.order_type == OrderType.MARKET
    assert order.product_type == ProductType.MIS
    assert order.status == OrderStatus.FILLED
    assert order.quantity == 100
    assert order.filled_quantity == 100
    assert order.average_price == 250.0
    assert order.price == 250.0
    assert order.trigger_price is None
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)


def test_from_kite_maps_status_aliases() -> None:
    """
    Broker status aliases should be normalized into Falcon status values.
    """

    instrument = Instrument(
        symbol="BANKNIFTY",
        exchange="NSE",
        instrument_token=260105,
        lot_size=25,
        tick_size=0.05,
    )

    payload = {
        "order_id": "broker-order-2",
        "tradingsymbol": "BANKNIFTY",
        "exchange": "NSE",
        "transaction_type": "SELL",
        "quantity": 50,
        "product": "CNC",
        "order_type": "SL-M",
        "status": "TRIGGER PENDING",
        "filled_quantity": 0,
        "average_price": 0.0,
        "price": None,
        "trigger_price": 100.0,
        "order_timestamp": "2024-01-01T10:00:00",
        "exchange_update_timestamp": "2024-01-01T10:00:00",
    }

    order = OrderResponseMapper.from_kite(instrument, payload)

    assert order.status == OrderStatus.OPEN
    assert order.order_type == OrderType.SL_MARKET
    assert order.product_type == ProductType.CNC
