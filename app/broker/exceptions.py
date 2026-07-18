"""
Broker-specific exceptions for Project Falcon.
"""

from __future__ import annotations


class BrokerError(Exception):
    """
    Base exception for all broker-related errors.
    """


class BrokerConfigurationError(BrokerError):
    """
    Raised when broker configuration is invalid.
    """


class BrokerConnectionError(BrokerError):
    """
    Raised when a broker connection cannot be established.
    """


class BrokerAuthenticationError(BrokerError):
    """
    Raised when broker authentication fails.
    """


class BrokerOrderError(BrokerError):
    """
    Raised when an order request fails.
    """


class BrokerMarketDataError(BrokerError):
    """
    Raised when market data cannot be retrieved.
    """