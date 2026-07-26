"""
Backtest factory bridge for Project Falcon.

Creates isolated BacktestApplicationFactory instances from immutable
BacktestConfig objects.

Responsibilities
----------------
- Build BacktestApplicationFactory instances.
- Preserve dependency injection boundaries.
- Remain stateless.

The bridge intentionally does NOT implement:

- Backtest execution
- Strategy creation
- Optimization
- Reporting
"""

from __future__ import annotations

from app.backtest.application_factory import (
    BacktestApplicationFactory,
)
from app.backtest.backtest_config import (
    BacktestConfig,
)


class BacktestFactoryBridge:
    """
    Stateless bridge producing BacktestApplicationFactory objects.
    """

    def create(
        self,
        config: BacktestConfig,
    ) -> BacktestApplicationFactory:
        """
        Create a new BacktestApplicationFactory.

        Parameters
        ----------
        config
            Immutable runtime configuration.

        Returns
        -------
        BacktestApplicationFactory
        """

        if not isinstance(
            config,
            BacktestConfig,
        ):
            raise TypeError(
                "config must be a BacktestConfig."
            )

        return BacktestApplicationFactory(
            config=config,
        )