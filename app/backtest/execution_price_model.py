"""
Execution price model for Project Falcon.

Provides deterministic execution price adjustments used during
historical backtesting. The model simulates slippage by adjusting
market prices for BUY and SELL executions.

Responsibilities
----------------
- Calculate BUY execution prices.
- Calculate SELL execution prices.
- Apply deterministic slippage.

The ExecutionPriceModel intentionally does NOT implement:

- Order execution
- Transaction cost calculations
- Portfolio accounting
- Performance analytics
- Broker-specific execution logic
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionPriceModel:
    """
    Immutable execution price model.

    Parameters
    ----------
    slippage_per_unit
        Fixed slippage applied to every traded unit.

        Example
        -------
        Market Price : 25000.00

        BUY  -> 25000.05

        SELL -> 24999.95
    """

    slippage_per_unit: float = 0.0

    def __post_init__(self) -> None:
        """
        Validate model parameters.

        Raises
        ------
        TypeError
            If slippage_per_unit is not numeric.

        ValueError
            If slippage_per_unit is negative.
        """

        if not isinstance(
            self.slippage_per_unit,
            (int, float),
        ):
            raise TypeError(
                "slippage_per_unit must be numeric."
            )

        if self.slippage_per_unit < 0:
            raise ValueError(
                "slippage_per_unit cannot be negative."
            )

    def buy_price(
        self,
        market_price: float,
    ) -> float:
        """
        Calculate BUY execution price.

        Parameters
        ----------
        market_price
            Current market price.

        Returns
        -------
        float
            Simulated BUY fill price.
        """

        if market_price < 0:
            raise ValueError(
                "market_price cannot be negative."
            )

        return (
            market_price
            + self.slippage_per_unit
        )

    def sell_price(
        self,
        market_price: float,
    ) -> float:
        """
        Calculate SELL execution price.

        Parameters
        ----------
        market_price
            Current market price.

        Returns
        -------
        float
            Simulated SELL fill price.
        """

        if market_price < 0:
            raise ValueError(
                "market_price cannot be negative."
            )

        return (
            market_price
            - self.slippage_per_unit
        )