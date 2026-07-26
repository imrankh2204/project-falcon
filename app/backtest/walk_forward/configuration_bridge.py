"""
Walk-forward configuration bridge for Project Falcon.

This module derives immutable runtime configurations for each
walk-forward window from reusable base configurations.

Responsibilities
----------------
- Produce optimization configurations for training windows.
- Produce backtest configurations for validation windows.
- Preserve immutable configuration semantics.

The WalkForwardConfigurationBridge intentionally does NOT implement:

- Optimization execution
- Backtest execution
- Strategy creation
- Ranking
- Report generation
"""

from __future__ import annotations

from dataclasses import replace

from app.backtest.backtest_config import BacktestConfig
from app.backtest.date_range import DateRange
from app.backtest.optimization.config import (
    OptimizationConfig,
)
from app.backtest.walk_forward.window import (
    WalkForwardWindow,
)


class WalkForwardConfigurationBridge:
    """
    Produces immutable runtime configurations for each
    walk-forward iteration.
    """

    def __init__(
        self,
        *,
        optimization_config: OptimizationConfig,
        backtest_config: BacktestConfig,
    ) -> None:

        if not isinstance(
            optimization_config,
            OptimizationConfig,
        ):
            raise TypeError(
                "optimization_config must be an OptimizationConfig."
            )

        if not isinstance(
            backtest_config,
            BacktestConfig,
        ):
            raise TypeError(
                "backtest_config must be a BacktestConfig."
            )

        self._optimization_config = optimization_config
        self._backtest_config = backtest_config

    def optimization_config(
        self,
        window: WalkForwardWindow,
    ) -> OptimizationConfig:
        """
        Build an optimization configuration for the
        training period.
        """

        if not isinstance(
            window,
            WalkForwardWindow,
        ):
            raise TypeError(
                "window must be a WalkForwardWindow."
            )

        return replace(
            self._optimization_config,
            date_range=DateRange(
                start_time=window.training_start,
                end_time=window.training_end,
            ),
        )

    def backtest_config(
        self,
        window: WalkForwardWindow,
    ) -> BacktestConfig:
        """
        Build a backtest configuration for the
        validation period.
        """

        if not isinstance(
            window,
            WalkForwardWindow,
        ):
            raise TypeError(
                "window must be a WalkForwardWindow."
            )

        return replace(
            self._backtest_config,
            date_range=DateRange(
                start_time=window.validation_start,
                end_time=window.validation_end,
            ),
        )