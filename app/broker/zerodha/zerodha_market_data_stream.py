"""
Concrete Zerodha MarketDataStream implementation.

Adapts Zerodha's WebSocket streaming interface to Falcon's broker-
independent MarketDataStream abstraction.

Responsibilities
----------------
- Connect to the broker market data stream.
- Disconnect from the broker market data stream.
- Subscribe to instrument tokens.
- Unsubscribe from instrument tokens.
- Forward broker callbacks to Falcon.
- Translate broker exceptions into Falcon exceptions.

The implementation intentionally does NOT implement:

- Tick parsing
- Trading logic
- Event dispatch
- Reconnection
- Retry logic
- Authentication
"""

from __future__ import annotations

from collections.abc import Callable

from kiteconnect import KiteTicker

from app.broker.zerodha.exception_mapper import (
    ExceptionMapper,
)
from app.broker.zerodha.session_manager import (
    SessionManager,
)
from app.live.market_data_stream import (
    MarketDataStream,
)


class ZerodhaMarketDataStream(
    MarketDataStream,
):
    """
    Concrete MarketDataStream backed by KiteTicker.
    """

    def __init__(
        self,
        *,
        session_manager: SessionManager,
    ) -> None:
        """
        Initialize the market data stream.
        """

        if not isinstance(
            session_manager,
            SessionManager,
        ):
            raise TypeError(
                "session_manager must be a SessionManager."
            )

        self._session_manager = session_manager

        self._tick_handler: Callable[
            [list[dict]],
            None,
        ] | None = None

        self._connect_handler: Callable[
            [],
            None,
        ] | None = None

        self._close_handler: Callable[
            [],
            None,
        ] | None = None

        self._error_handler: Callable[
            [Exception],
            None,
        ] | None = None

        self.ticker.on_ticks = self._on_ticks
        self.ticker.on_connect = self._on_connect
        self.ticker.on_close = self._on_close
        self.ticker.on_error = self._on_error

    @property
    def session_manager(
        self,
    ) -> SessionManager:
        """
        Return the configured session manager.
        """

        return self._session_manager

    @property
    def ticker(
        self,
    ) -> KiteTicker:
        """
        Return the authenticated KiteTicker instance.
        """

        return self._session_manager.kite_ticker

    def connect(
        self,
    ) -> None:
        """
        Connect to the market data stream.
        """

        try:
            self.ticker.connect(
                threaded=True,
            )

        except Exception as exc:
            raise ExceptionMapper.translate(
                exc,
            ) from exc

    def disconnect(
        self,
    ) -> None:
        """
        Disconnect from the market data stream.
        """

        try:
            self.ticker.close()

        except Exception as exc:
            raise ExceptionMapper.translate(
                exc,
            ) from exc

    def subscribe(
        self,
        instrument_tokens: tuple[
            int,
            ...,
        ],
    ) -> None:
        """
        Subscribe to instrument tokens.
        """

        if not isinstance(
            instrument_tokens,
            tuple,
        ):
            raise TypeError(
                "instrument_tokens must be a tuple."
            )

        try:
            self.ticker.subscribe(
                list(
                    instrument_tokens,
                ),
            )

        except Exception as exc:
            raise ExceptionMapper.translate(
                exc,
            ) from exc

    def unsubscribe(
        self,
        instrument_tokens: tuple[
            int,
            ...,
        ],
    ) -> None:
        """
        Unsubscribe from instrument tokens.
        """

        if not isinstance(
            instrument_tokens,
            tuple,
        ):
            raise TypeError(
                "instrument_tokens must be a tuple."
            )

        try:
            self.ticker.unsubscribe(
                list(
                    instrument_tokens,
                ),
            )

        except Exception as exc:
            raise ExceptionMapper.translate(
                exc,
            ) from exc

    def set_tick_handler(
        self,
        handler: Callable[
            [list[dict]],
            None,
        ],
    ) -> None:
        """
        Register the Falcon tick handler.
        """

        if not callable(
            handler,
        ):
            raise TypeError(
                "handler must be callable."
            )

        self._tick_handler = handler

    def set_connect_handler(
        self,
        handler: Callable[
            [],
            None,
        ],
    ) -> None:
        """
        Register the Falcon connect handler.
        """

        if not callable(
            handler,
        ):
            raise TypeError(
                "handler must be callable."
            )

        self._connect_handler = handler

    def set_close_handler(
        self,
        handler: Callable[
            [],
            None,
        ],
    ) -> None:
        """
        Register the Falcon close handler.
        """

        if not callable(
            handler,
        ):
            raise TypeError(
                "handler must be callable."
            )

        self._close_handler = handler

    def set_error_handler(
        self,
        handler: Callable[
            [Exception],
            None,
        ],
    ) -> None:
        """
        Register the Falcon error handler.
        """

        if not callable(
            handler,
        ):
            raise TypeError(
                "handler must be callable."
            )

        self._error_handler = handler

    def _on_ticks(
        self,
        ws: KiteTicker,
        ticks: list[dict],
    ) -> None:
        """
        Forward broker ticks to Falcon.
        """

        if self._tick_handler is None:
            return

        self._tick_handler(
            ticks,
        )

    def _on_connect(
        self,
        ws: KiteTicker,
        response: dict,
    ) -> None:
        """
        Forward broker connect events.
        """

        if self._connect_handler is None:
            return

        self._connect_handler()

    def _on_close(
        self,
        ws: KiteTicker,
        code: int,
        reason: str,
    ) -> None:
        """
        Forward broker close events.
        """

        if self._close_handler is None:
            return

        self._close_handler()

    def _on_error(
        self,
        ws: KiteTicker,
        code: int,
        reason: str,
    ) -> None:
        """
        Forward broker error events.
        """

        if self._error_handler is None:
            return

        self._error_handler(
            RuntimeError(
                f"KiteTicker error {code}: {reason}"
            )
        )