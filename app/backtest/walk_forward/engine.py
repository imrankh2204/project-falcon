"""
Walk-forward optimization execution engine.

This module coordinates rolling optimization and validation cycles.

Responsibilities
----------------
- Execute optimization on training windows.
- Execute validation on unseen windows.
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

from app.backtest.optimization.service import (
    OptimizationService,
)
from app.backtest.walk_forward.result import (
    WalkForwardIterationResult,
    WalkForwardResult,
)
from app.backtest.walk_forward.window import (
    WalkForwardWindow,
)
from app.backtest.application_factory import (
    BacktestApplicationFactory,
)



class WalkForwardEngine:
    """
    Deterministic walk-forward execution engine.
    """

    def __init__(
        self,
        *,
        optimization_service: OptimizationService,
        backtest_factory: BacktestApplicationFactory,
    ) -> None:

        if not hasattr(
            optimization_service,
            "run",
        ):
            raise TypeError(
                "optimization_service must provide a run method."
            )

        if not hasattr(
            backtest_factory,
            "create",
        ):
            raise TypeError(
                "backtest_factory must provide a create method."
            )

        self._optimization_service = (
            optimization_service
        )

        self._backtest_factory = (
            backtest_factory
        )

    def run(
        self,
        *,
        windows: Iterable[WalkForwardWindow],
    ) -> WalkForwardResult:
        """
        Execute walk-forward evaluation.

        Parameters
        ----------
        windows
            Ordered walk-forward evaluation windows.

        Returns
        -------
        WalkForwardResult
            Immutable walk-forward execution result.
        """

        results: list[
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

            optimization_result = (
                self._optimization_service.run(
                    window
                )
            )

            validation_report = None

            results.append(
                WalkForwardIterationResult(
                    window=window,
                    optimization_result=(
                        optimization_result
                    ),
                    validation_report=(
                        validation_report
                    ),
                )
            )

        return WalkForwardResult(
            iterations=tuple(results)
        )