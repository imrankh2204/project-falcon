"""
Execution cost model for Project Falcon.

Provides deterministic transaction cost calculations used during
historical backtesting. The model is intentionally broker-independent
and contains no execution, portfolio, or reporting logic.

Responsibilities
----------------
- Calculate commission.
- Calculate slippage.
- Calculate total execution cost.

The ExecutionCostModel intentionally does NOT implement:

- Order execution
- Broker-specific fee schedules
- Portfolio accounting
- Performance analytics
- Tax calculations
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionCostModel:
    """
    Immutable execution cost model.

    Parameters
    ----------
    commission_rate
        Commission rate expressed as a decimal fraction.

        Example:
            0.001 == 0.10%

    slippage_per_unit
        Fixed slippage applied per traded unit.
    """

    commission_rate: float = 0.0
    slippage_per_unit: float = 0.0

    def __post_init__(self) -> None:
        """
        Validate model parameters.

        Raises
        ------
        TypeError
            If values are not numeric.

        ValueError
            If values are negative.
        """

        if not isinstance(
            self.commission_rate,
            (int, float),
        ):
            raise TypeError(
                "commission_rate must be numeric."
            )

        if not isinstance(
            self.slippage_per_unit,
            (int, float),
        ):
            raise TypeError(
                "slippage_per_unit must be numeric."
            )

        if self.commission_rate < 0:
            raise ValueError(
                "commission_rate cannot be negative."
            )

        if self.slippage_per_unit < 0:
            raise ValueError(
                "slippage_per_unit cannot be negative."
            )

    def commission(
        self,
        trade_value: float,
    ) -> float:
        """
        Calculate commission.

        Parameters
        ----------
        trade_value
            Total monetary value of the trade.

        Returns
        -------
        float
            Commission amount.
        """

        if trade_value < 0:
            raise ValueError(
                "trade_value cannot be negative."
            )

        return trade_value * float(
            self.commission_rate
        )

    def slippage(
        self,
        quantity: int,
    ) -> float:
        """
        Calculate slippage cost.

        Parameters
        ----------
        quantity
            Number of traded units.

        Returns
        -------
        float
            Total slippage cost.
        """

        if quantity < 0:
            raise ValueError(
                "quantity cannot be negative."
            )

        return quantity * float(
            self.slippage_per_unit
        )

    def total_cost(
        self,
        *,
        trade_value: float,
        quantity: int,
    ) -> float:
        """
        Calculate total execution cost.

        Parameters
        ----------
        trade_value
            Total monetary value of the trade.

        quantity
            Number of traded units.

        Returns
        -------
        float
            Total execution cost.
        """

        return (
            self.commission(trade_value)
            + self.slippage(quantity)
        )