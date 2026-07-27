"""
Immutable broker order identifier.

Defines the strongly typed identifier used throughout the live trading
layer instead of raw string values.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderId:
    """
    Immutable broker order identifier.

    Parameters
    ----------
    value
        Broker-generated order identifier.
    """

    value: str

    def __post_init__(self) -> None:
        """
        Validate identifier.

        Raises
        ------
        TypeError
            If the identifier is not a string.

        ValueError
            If the identifier is empty.
        """

        if not isinstance(
            self.value,
            str,
        ):
            raise TypeError(
                "value must be a string."
            )

        if not self.value.strip():
            raise ValueError(
                "value cannot be empty."
            )

    def __str__(self) -> str:
        """
        Return the underlying identifier.
        """

        return self.value