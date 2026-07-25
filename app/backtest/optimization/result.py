"""
Immutable optimization result for Project Falcon.

This module defines the immutable association between a strategy parameter
configuration and the completed backtest report produced for that
configuration.

The OptimizationResult intentionally contains no calculation logic and
serves only as a transport model.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.backtest.reporting.report import BacktestReport
from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


@dataclass(frozen=True, slots=True)
class OptimizationResult:
    """
    Immutable optimization result.

    Attributes
    ----------
    parameters
        EMA parameter configuration evaluated.

    report
        Completed immutable backtest report produced for the parameter set.
    """

    parameters: EMACrossoverParameters

    report: BacktestReport