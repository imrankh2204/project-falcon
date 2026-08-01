"""
Session manager for Zerodha authentication.

Coordinates authenticated session lifecycle while remaining isolated
from broker-specific implementation details.

Responsibilities
----------------
- Restore persisted sessions.
- Authenticate when required.
- Persist authenticated sessions.
- Expose immutable broker sessions.
- Logout cleanly.

The SessionManager intentionally does NOT implement:

- Kite SDK communication
- Order execution
- Quote retrieval
- Position management
"""

from __future__ import annotations

from kiteconnect import KiteConnect
from kiteconnect import KiteTicker

from app.broker.zerodha.authentication import (
    ZerodhaAuthentication,
)
from app.broker.zerodha.token_store import (
    TokenStore,
)
from app.live.broker_session import (
    BrokerSession,
)


class SessionManager:
    """
    Coordinates authenticated broker session lifecycle.
    """

    def __init__(
        self,
        *,
        authentication: ZerodhaAuthentication,
        token_store: TokenStore,
    ) -> None:
        if not isinstance(
            authentication,
            ZerodhaAuthentication,
        ):
            raise TypeError(
                "authentication must be a ZerodhaAuthentication."
            )

        if not isinstance(
            token_store,
            TokenStore,
        ):
            raise TypeError(
                "token_store must be a TokenStore."
            )

        self._authentication = authentication
        self._token_store = token_store
        self._session: BrokerSession | None = None
        self._kite: KiteConnect | None = None
        self._kite_ticker: KiteTicker | None = None

    @property
    def session(
        self,
    ) -> BrokerSession | None:
        """
        Return the current authenticated session.
        """

        return self._session

    @property
    def kite(
        self,
    ) -> KiteConnect:
        """
        Return the authenticated Kite client.
        """

        if self._kite is None:
            raise RuntimeError(
                "No authenticated Kite client."
            )

        return self._kite

    @property
    def kite_ticker(
        self,
    ) -> KiteTicker:
        """
        Return the authenticated KiteTicker client.
        """

        if self._kite_ticker is None:
            raise RuntimeError(
                "No authenticated KiteTicker client."
            )

        return self._kite_ticker

    @property
    def is_authenticated(
        self,
    ) -> bool:
        """
        Return True when a valid authenticated session exists.
        """

        return (
            self._session is not None
            and self._kite is not None
            and not self._session.is_expired
        )

    def authenticate(
        self,
    ) -> BrokerSession:
        """
        Authenticate with Zerodha.

        Returns
        -------
        BrokerSession
            Authenticated immutable broker session.
        """

        result = self._authentication.authenticate()

        self._session = result.session

        self._kite = result.kite

        self._kite_ticker = result.kite_ticker

        self._token_store.save(
            result.session,
        )

        return result.session

    def restore(
        self,
    ) -> BrokerSession | None:
        """
        Restore a persisted broker session.

        Returns
        -------
        BrokerSession | None
            Restored session if available and valid.
        """

        session = self._token_store.load()

        if session is None:
            return None

        if session.is_expired:
            self._token_store.clear()
            return None

        self._session = session

        return session

    def get_session(
        self,
    ) -> BrokerSession:
        """
        Return an authenticated broker session.

        Restores a persisted session when possible and performs
        authentication if no valid session exists.
        """

        if self.is_authenticated:
            return self._session  # type: ignore[return-value]

        restored = self.restore()

        if restored is not None:
            return restored

        return self.authenticate()

    def logout(
        self,
    ) -> None:
        """
        Remove the active authenticated session.
        """

        self._token_store.clear()
        self._session = None
        self._kite = None
        self._kite_ticker = None