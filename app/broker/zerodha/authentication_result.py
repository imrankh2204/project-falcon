"""
Authentication result for Zerodha authentication.

Bundles the immutable authenticated broker session together with the
authenticated Kite SDK clients.

Responsibilities
----------------
- Transport authentication outcome.
- Keep session and SDK clients synchronized.
- Remain immutable after creation.

The model intentionally does NOT implement:

- Authentication
- Session persistence
- Token refresh
- Broker operations
"""

from __future__ import annotations

from dataclasses import dataclass

from kiteconnect import KiteConnect
from kiteconnect import KiteTicker

from app.live.broker_session import BrokerSession


@dataclass(frozen=True, slots=True)
class AuthenticationResult:
    """
    Immutable authentication result.
    """

    session: BrokerSession

    kite: KiteConnect

    kite_ticker: KiteTicker

    def __post_init__(self) -> None:
        """
        Validate the authentication result.
        """

        if not isinstance(
            self.session,
            BrokerSession,
        ):
            raise TypeError(
                "session must be a BrokerSession."
            )

        if not isinstance(
            self.kite,
            KiteConnect,
        ):
            raise TypeError(
                "kite must be a KiteConnect."
            )

        if not isinstance(
            self.kite_ticker,
            KiteTicker,
        ):
            raise TypeError(
                "kite_ticker must be a KiteTicker."
            )