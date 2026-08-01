"""
Zerodha broker implementation for Project Falcon.

This package contains the concrete implementation of Falcon's broker
abstractions using the Kite Connect API.

Architectural Rules
-------------------
Only this package may directly depend on the Kite SDK.

Everything outside this package communicates exclusively through the
broker contracts defined under app.live.
"""

from .authentication import ZerodhaAuthentication

__all__ = [
    "ZerodhaAuthentication",
]