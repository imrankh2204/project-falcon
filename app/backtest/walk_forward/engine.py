"""
Walk-forward optimization execution engine for Project Falcon.

This module coordinates rolling optimization and out-of-sample
validation execution.

Responsibilities
----------------
- Execute optimization on training windows.
- Select optimized strategy parameters.
- Execute validation backtests.
- Produce immutable walk-forward results.

The WalkForwardEngine intentionally does NOT implement:

- Strategy logic
- Parameter generation
- Ranking
- Performance calculations
- Report exporting
"""

from __future__ import annotations

from collections.abc import Iterable

from app.backtest.backtest_factory_bridge import (
    BacktestFactoryBridge,
)

from app.backtest.optimization.service import (
    OptimizationService,
)

from app.backtest.walk_forward.configuration_bridge import (
    WalkForwardConfigurationBridge,
)

from app.backtest.walk_forward.result import (
    WalkForwardIterationResult,
    WalkForwardResult,
)

from app.backtest.walk_forward.window import (
    WalkForwardWindow,
)

from app.strategies.strategy_factory import (
    StrategyFactory,
)


class WalkForwardEngine:
    """
    Deterministic walk-forward execution engine.

    Each execution follows:

    Training Window
        |
        v
    OptimizationService
        |
        v
    Best Parameters
        |
        v
    StrategyFactory
        |
        v
    Validation Backtest
        |
        v
    WalkForwardIterationResult
    """

    def __init__(
        self,
        *,
        optimization_service: OptimizationService,
        configuration_bridge: WalkForwardConfigurationBridge,
        backtest_factory_bridge: BacktestFactoryBridge,
    ) -> None:

        if not isinstance(
            optimization_service,
            OptimizationService,
        ):
            raise TypeError(
                "optimization_service must be an OptimizationService."
            )

        if not isinstance(
            configuration_bridge,
            WalkForwardConfigurationBridge,
        ):
            raise TypeError(
                "configuration_bridge must be a WalkForwardConfigurationBridge."
            )

        if not isinstance(
            backtest_factory_bridge,
            BacktestFactoryBridge,
        ):
            raise TypeError(
                "backtest_factory_bridge must be a BacktestFactoryBridge."
            )

        self._optimization_service = (
            optimization_service
        )

        self._configuration_bridge = (
            configuration_bridge
        )

        self._backtest_factory_bridge = (
            backtest_factory_bridge
        )

    def run(
        self,
        *,
        windows: Iterable[WalkForwardWindow],
    ) -> WalkForwardResult:
        """
        Execute walk-forward optimization.

        Parameters
        ----------
        windows
            Ordered walk-forward evaluation windows.

        Returns
        -------
        WalkForwardResult
            Immutable aggregated walk-forward result.
        """

        iterations: list[
            WalkForwardIterationResult
        ] = []

        for window in windows:

            if not isinstance(
                window,
                WalkForwardWindow,
            ):
                raise TypeError(
                    "windows must contain WalkForwardWindow objects."
                )

            #
            # Training configuration
            #

            optimization_config = (
                self._configuration_bridge
                .optimization_config(
                    window
                )
            )

            #
            # Execute optimization
            #

            optimization_report = (
                self._optimization_service.run(
                    optimization_config
                )
            )

            #
            # Build strategy using optimized parameters
            #

            strategy = (
                StrategyFactory.create(
                    optimization_report
                    .best_parameters
                )
            )

            #
            # Validation configuration
            #

            validation_config = (
                self._configuration_bridge
                .backtest_config(
                    window
                )
            )

            #
            # Execute validation backtest
            #

            application_factory = (
                self._backtest_factory_bridge
                .create(
                    validation_config
                )
            )

            application = (
                application_factory
                .create(
                    strategy
                )
            )

            validation_report = (
                application.run()
            )

            #
            # Store immutable iteration snapshot
            #

            iterations.append(
                WalkForwardIterationResult(
                    window=window,
                    optimization_result=(
                        optimization_report
                        .best_result
                    ),
                    validation_report=(
                        validation_report
                    ),
                )
            )

        return WalkForwardResult(
            iterations=tuple(iterations)
        )