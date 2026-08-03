"""
Broker exception translation for Zerodha.

This module converts broker-specific exceptions into Falcon's
broker-independent exception hierarchy.

Responsibilities
----------------
- Translate Kite exceptions.
- Preserve broker isolation.
- Hide third-party exception types.

Concrete mappings will be added during the live API integration phase.
"""

from __future__ import annotations

from app.live.exceptions import BrokerError


class ExceptionMapper:
    """
    Stateless exception translator.
    """

    @staticmethod
    def translate(
        exception: Exception,
    ) -> BrokerError:
        """
        Translate a broker exception.

        Parameters
        ----------
        exception
            Original broker exception.

        Returns
        -------
        BrokerError
            Falcon broker-independent exception.
        """

        return BrokerError(
            str(exception)
        )