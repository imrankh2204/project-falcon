"""
Optimization application for Project Falcon.

This module provides the top-level executable optimization application.

Responsibilities
----------------
- Own immutable optimization configuration.
- Delegate optimization execution to OptimizationService.
- Return immutable OptimizationReport.

The OptimizationApplication intentionally does NOT implement:

- Strategy construction
- Parameter generation
- Workflow orchestration
- Ranking
- Console rendering
"""

from __future__ import annotations

from app.backtest.optimization.config import (
    OptimizationConfig,
)
from app.backtest.optimization.report import (
    OptimizationReport,
)
from app.backtest.optimization.service import (
    OptimizationService,
)


class OptimizationApplication:
    """
    Executable optimization application.

    This object owns immutable optimization configuration and delegates
    execution to OptimizationService.
    """

    def __init__(
        self,
        *,
        config: OptimizationConfig,
        service: OptimizationService,
    ) -> None:

        if not isinstance(
            config,
            OptimizationConfig,
        ):
            raise TypeError(
                "config must be an OptimizationConfig."
            )

        if not isinstance(
            service,
            OptimizationService,
        ):
            raise TypeError(
                "service must be an OptimizationService."
            )

        self._config = config
        self._service = service

    @property
    def config(
        self,
    ) -> OptimizationConfig:
        """
        Return immutable optimization configuration.
        """

        return self._config

    def run(
        self,
    ) -> OptimizationReport:
        """
        Execute optimization.

        Returns
        -------
        OptimizationReport
            Immutable optimization report.
        """

        return self._service.run(
            self._config
        )