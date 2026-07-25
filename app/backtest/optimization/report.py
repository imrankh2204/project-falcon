"""
Immutable optimization reporting model for Project Falcon.

This module defines the immutable reporting contract representing the
results of a completed optimization run.

The report is presentation-facing only and intentionally contains no
business logic, ranking logic, or calculations.

Responsibilities
----------------
- Store optimization results.
- Preserve deterministic ordering.
- Provide an immutable reporting contract.

The OptimizationReport intentionally does NOT implement:

- Ranking
- Filtering
- Parameter generation
- Backtest execution
- Report rendering
"""

from __future__ import annotations

from dataclasses import dataclass

from app.backtest.optimization.result import OptimizationResult


@dataclass(frozen=True, slots=True)
class OptimizationReport:
    """
    Immutable optimization report.

    Attributes
    ----------
    results
        Optimization results in deterministic execution order.
    """

    results: tuple[OptimizationResult, ...]