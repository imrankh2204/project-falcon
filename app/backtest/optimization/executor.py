"""
Optimization execution coordinator for Project Falcon.

This module connects optimization parameters with the existing backtesting
pipeline.

Responsibilities
----------------
- Create strategy instances through StrategyFactory.
- Create isolated BacktestApplication instances.
- Execute isolated backtests.
- Convert completed backtest reports into OptimizationResult.

The OptimizationExecutor intentionally does NOT implement:

- Parameter generation
- Ranking
- Performance calculations
- Trading execution
- Portfolio management
"""

from __future__ import annotations

from app.backtest.application_factory import (
    BacktestApplicationFactory,
)
from app.backtest.optimization.result import (
    OptimizationResult,
)
from app.backtest.reporting.report import (
    BacktestReport,
)
from app.core.backtest_application import (
    BacktestApplication,
)
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)
from app.strategies.strategy_factory import (
    StrategyFactory,
)


class OptimizationExecutor:
    """
    Executes a single optimization parameter configuration.

    The executor is stateless and deterministic. Each execution
    produces an independent OptimizationResult.
    """

    def __init__(
        self,
        *,
        strategy_factory: StrategyFactory,
        application_factory: BacktestApplicationFactory,
    ) -> None:

        if not isinstance(
            strategy_factory,
            StrategyFactory,
        ):
            raise TypeError(
                "strategy_factory must be a StrategyFactory."
            )

        if not isinstance(
            application_factory,
            BacktestApplicationFactory,
        ):
            raise TypeError(
                "application_factory must be a BacktestApplicationFactory."
            )

        self._strategy_factory = strategy_factory
        self._application_factory = application_factory

    def execute(
        self,
        parameters: EMACrossoverParameters,
    ) -> OptimizationResult:
        """
        Execute one optimization iteration.

        Parameters
        ----------
        parameters
            Strategy configuration to evaluate.

        Returns
        -------
        OptimizationResult
            Immutable optimization result.
        """

        strategy = self._strategy_factory.create(
            parameters
        )

        application: BacktestApplication = (
            self._application_factory.create(
                strategy
            )
        )

        report: BacktestReport = (
            application.run()
        )

        return OptimizationResult(
            parameters=parameters,
            report=report,
        )