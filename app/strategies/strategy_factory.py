"""
Strategy factory for Project Falcon.

This module centralizes construction of concrete trading strategies from
immutable parameter objects.

Responsibilities
----------------
- Construct strategy instances.
- Hide concrete strategy constructors.
- Remain stateless and deterministic.

The factory intentionally does NOT implement:

- Strategy logic
- Indicator calculations
- Dependency injection
- Replay orchestration
- Trading logic
"""

from __future__ import annotations

from app.strategies.ema_crossover import EMACrossoverStrategy
from app.strategies.ema_parameters import EMACrossoverParameters
from app.strategies.strategy import Strategy


class StrategyFactory:
    """
    Stateless factory for creating strategy instances.
    """

    @staticmethod
    def create(
        parameters: EMACrossoverParameters,
    ) -> Strategy:
        """
        Create an EMA crossover strategy.

        Parameters
        ----------
        parameters
            Immutable EMA strategy configuration.

        Returns
        -------
        Strategy
            Configured strategy instance.
        """

        if not isinstance(
            parameters,
            EMACrossoverParameters,
        ):
            raise TypeError(
                "parameters must be an EMACrossoverParameters."
            )

        return EMACrossoverStrategy(
            fast_period=parameters.fast_period,
            slow_period=parameters.slow_period,
        )