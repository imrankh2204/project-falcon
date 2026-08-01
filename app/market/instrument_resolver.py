"""
Broker-independent instrument resolver contract.

Provides immutable Instrument lookup for broker adapters.

Responsibilities
----------------
- Resolve immutable Instrument objects.
- Remain broker independent.
- Hide instrument lookup implementation.

The resolver intentionally does NOT implement:

- Broker communication
- Instrument downloads
- Instrument caching
- Symbol normalization
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.market.instrument import Instrument


class InstrumentResolver(ABC):
    """
    Abstract instrument resolver.

    Implementations provide immutable Instrument lookup for broker
    adapters.
    """

    @abstractmethod
    def resolve(
        self,
        exchange: str,
        symbol: str,
    ) -> Instrument:
        """
        Resolve an immutable Instrument.

        Parameters
        ----------
        exchange
            Broker exchange.

        symbol
            Broker trading symbol.

        Returns
        -------
        Instrument
            Fully populated immutable instrument.

        Raises
        ------
        LookupError
            If the instrument cannot be resolved.
        """