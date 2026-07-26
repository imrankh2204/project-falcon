"""
Walk-forward optimization service for Project Falcon.

This module provides the public orchestration layer for
walk-forward execution.

Responsibilities
----------------
- Validate walk-forward configuration.
- Delegate execution to WalkForwardEngine.
- Return immutable WalkForwardResult.

The WalkForwardService intentionally does NOT implement:

- Window generation
- Optimization execution
- Backtest execution
- Performance calculations
- Report exporting
"""

from __future__ import annotations

from collections.abc import Iterable

from app.backtest.walk_forward.config import (
    WalkForwardConfig,
)
from app.backtest.walk_forward.engine import (
    WalkForwardEngine,
)
from app.backtest.walk_forward.result import (
    WalkForwardResult,
)
from app.backtest.walk_forward.window import (
    WalkForwardWindow,
)


class WalkForwardService:
    """
    Public orchestration service for walk-forward execution.
    """

    def __init__(
        self,
        *,
        engine: WalkForwardEngine,
    ) -> None:

        if not isinstance(
            engine,
            WalkForwardEngine,
        ):
            raise TypeError(
                "engine must be a WalkForwardEngine."
            )

        self._engine = engine

    def run(
        self,
        *,
        config: WalkForwardConfig,
        windows: Iterable[WalkForwardWindow],
    ) -> WalkForwardResult:
        """
        Execute walk-forward optimization.

        Parameters
        ----------
        config
            Walk-forward execution configuration.

        windows
            Ordered evaluation windows.

        Returns
        -------
        WalkForwardResult
            Immutable walk-forward execution result.
        """

        if not isinstance(
            config,
            WalkForwardConfig,
        ):
            raise TypeError(
                "config must be a WalkForwardConfig."
            )

        return self._engine.run(
            windows=windows
        )