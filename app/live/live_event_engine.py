"""
Live Event Engine.

Coordinates the flow of live market events between the broker transport
layer and Falcon's internal event pipeline.

Responsibilities
----------------
- Register with the MarketDataStream.
- Receive raw broker tick batches.
- Translate broker ticks into Falcon domain objects.
- Publish broker-independent LiveEvent objects.
- Remain broker independent.

The engine intentionally does NOT implement:

- Indicator calculations
- Strategy execution
- Order management
- Broker SDK communication
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from app.live.live_event import (
    LiveEvent,
)
from app.live.live_tick import (
    LiveTick,
)
from app.live.market_data_stream import (
    MarketDataStream,
)


class LiveEventEngine:
    """
    Coordinates the live event pipeline.
    """

    def __init__(
        self,
        *,
        market_data_stream: MarketDataStream,
    ) -> None:
        if not isinstance(
            market_data_stream,
            MarketDataStream,
        ):
            raise TypeError(
                "market_data_stream must be a "
                "MarketDataStream."
            )

        self._market_data_stream = (
            market_data_stream
        )

        self._event_handler: Callable[
            [LiveEvent],
            None,
        ] | None = None

        self._market_data_stream.set_tick_handler(
            self._on_ticks,
        )

    @property
    def market_data_stream(
        self,
    ) -> MarketDataStream:
        """
        Return the configured market data stream.
        """

        return self._market_data_stream

    def set_event_handler(
        self,
        handler: Callable[
            [LiveEvent],
            None,
        ],
    ) -> None:
        """
        Register the Falcon event handler.
        """

        if not callable(
            handler,
        ):
            raise TypeError(
                "handler must be callable."
            )

        self._event_handler = handler

    def start(
        self,
    ) -> None:
        """
        Start the live event engine.
        """

        self._market_data_stream.connect()

    def stop(
        self,
    ) -> None:
        """
        Stop the live event engine.
        """

        self._market_data_stream.disconnect()

    def _translate_tick(
        self,
        tick: dict,
    ) -> LiveTick:
        """
        Translate a broker tick into a Falcon LiveTick.
        """

        if not isinstance(
            tick,
            dict,
        ):
            raise TypeError(
                "tick must be a dict."
            )

        return LiveTick(
            instrument_token=tick[
                "instrument_token"
            ],
            last_price=tick[
                "last_price"
            ],
            volume=tick.get(
                "volume",
                0,
            ),
            open_interest=tick.get(
                "oi",
                0,
            ),
            timestamp=tick.get(
                "exchange_timestamp",
                datetime.now(),
            ),
        )

    def _on_ticks(
        self,
        ticks: list[dict],
    ) -> None:
        """
        Receive raw broker ticks and publish Falcon events.
        """

        if self._event_handler is None:
            return

        for tick in ticks:
            live_tick = self._translate_tick(
                tick,
            )

            event = LiveEvent(
                tick=live_tick,
            )

            self._event_handler(
                event,
            )