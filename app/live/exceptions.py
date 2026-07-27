"""
Broker-independent exceptions for Project Falcon.

This module defines the exception hierarchy used by the live trading
layer. Concrete broker adapters translate vendor-specific exceptions
into these broker-agnostic exceptions.

Responsibilities
----------------
- Define broker-independent exceptions.
- Preserve architecture isolation.
- Provide stable exception contracts.

The exceptions intentionally do NOT contain broker-specific logic.
"""

from __future__ import annotations


class BrokerError(Exception):
    """
    Base exception for all broker-related failures.
    """


class AuthenticationError(BrokerError):
    """
    Raised when broker authentication fails.
    """


class SessionExpiredError(BrokerError):
    """
    Raised when an authenticated broker session has expired.
    """


class NetworkError(BrokerError):
    """
    Raised when broker communication fails because of network issues.
    """


class OrderRejectedError(BrokerError):
    """
    Raised when a broker rejects an order request.
    """


class OrderNotFoundError(BrokerError):
    """
    Raised when a requested broker order cannot be located.
    """


class MarketClosedError(BrokerError):
    """
    Raised when an operation cannot be completed because the market
    is closed.
    """