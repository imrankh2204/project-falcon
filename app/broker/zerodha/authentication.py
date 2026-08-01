"""
Zerodha authentication contract.

Encapsulates authentication responsibilities for Kite Connect while
remaining isolated from the remainder of Project Falcon.

Responsibilities
----------------
- Authenticate with Kite Connect.
- Produce immutable authentication results.
- Hide Kite SDK authentication details.
- Translate broker failures into Falcon exceptions.

The interface intentionally does NOT implement:

- Order execution
- Quote retrieval
- Position management
- Session persistence
"""

from __future__ import annotations

from kiteconnect import KiteConnect
from abc import ABC
from abc import abstractmethod

from app.broker.zerodha.authentication_result import (
    AuthenticationResult,
)


class ZerodhaAuthentication(ABC):
    """
    Abstract authentication interface for Zerodha.

    Concrete implementations authenticate against Kite Connect and
    return both the immutable broker session and authenticated SDK
    client.
    """

    @abstractmethod
    def authenticate(
        self,
    ) -> AuthenticationResult:
        """
        Perform authentication.

        Returns
        -------
        AuthenticationResult
            Immutable authenticated session together with the
            authenticated Kite Connect client.
        """