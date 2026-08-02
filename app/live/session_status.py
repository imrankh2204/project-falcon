"""
Broker session lifecycle state definitions for Project Falcon.

Defines the immutable lifecycle states used by broker sessions.

The enum intentionally contains state representation only.
It does not implement authentication, refresh, reconnect,
or broker communication behavior.
"""

from __future__ import annotations

from enum import Enum


class SessionStatus(Enum):
    """
    Broker session lifecycle state.
    """

    CREATED = "created"

    AUTHENTICATING = "authenticating"

    AUTHENTICATED = "authenticated"

    EXPIRED = "expired"

    DISCONNECTED = "disconnected"

    FAILED = "failed"