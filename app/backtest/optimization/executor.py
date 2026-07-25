"""
Optimization execution coordinator for Project Falcon.

This module connects optimization parameters with the existing backtesting
pipeline.

Responsibilities
----------------
- Create strategy instances through StrategyFactory.
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

from app.backtest.reporting.builder import ReportBuilder
from app.backtest.optimization.result import OptimizationResult
from app.backtest.backtest_result import BacktestResult
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)
from app.strategies.strategy_factory import StrategyFactory


class OptimizationExecutor:
    """
    Executes a single optimization parameter configuration.

    The executor is stateless and deterministic. Each execution must produce
    an independent OptimizationResult.
    """

    def __init__(
        self,
        *,
        strategy_factory: StrategyFactory,
        backtest_runner,
        report_builder: ReportBuilder,
    ) -> None:

        if not isinstance(
            strategy_factory,
            StrategyFactory,
        ):
            raise TypeError(
                "strategy_factory must be a StrategyFactory."
            )

        if not callable(backtest_runner):
            raise TypeError(
                "backtest_runner must be callable."
            )

        if not isinstance(
            report_builder,
            ReportBuilder,
        ):
            raise TypeError(
                "report_builder must be a ReportBuilder."
            )

        self._strategy_factory = strategy_factory
        self._backtest_runner = backtest_runner
        self._report_builder = report_builder

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

        strategy = (
            self._strategy_factory.create(
                parameters
            )
        )

        result: BacktestResult = (
            self._backtest_runner(
                strategy
            )
        )

        report = (
            self._report_builder.build(
                result
            )
        )

        return OptimizationResult(
            parameters=parameters,
            report=report,
        )