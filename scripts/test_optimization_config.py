"""
Validation suite for OptimizationConfig.
"""

from __future__ import annotations

from app.backtest.optimization.config import (
    OptimizationConfig,
)
from app.backtest.optimization.ranking import (
    RankingMetric,
)


def test_valid_configuration() -> None:

    config = OptimizationConfig(
        fast_periods=(5, 9),
        slow_periods=(20, 30),
        ranking_metric=RankingMetric.NET_PROFIT,
        max_combinations=100,
    )

    assert config.fast_periods == (
        5,
        9,
    )

    assert config.slow_periods == (
        20,
        30,
    )

    assert (
        config.ranking_metric
        is RankingMetric.NET_PROFIT
    )

    assert (
        config.max_combinations
        == 100
    )


def test_empty_fast_periods() -> None:

    try:

        OptimizationConfig(
            fast_periods=(),
            slow_periods=(20,),
            ranking_metric=RankingMetric.NET_PROFIT,
        )

    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError."
    )


def test_empty_slow_periods() -> None:

    try:

        OptimizationConfig(
            fast_periods=(5,),
            slow_periods=(),
            ranking_metric=RankingMetric.NET_PROFIT,
        )

    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError."
    )


def test_invalid_max_combinations() -> None:

    try:

        OptimizationConfig(
            fast_periods=(5,),
            slow_periods=(20,),
            ranking_metric=RankingMetric.NET_PROFIT,
            max_combinations=0,
        )

    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError."
    )


def test_determinism() -> None:

    first = OptimizationConfig(
        fast_periods=(5, 9),
        slow_periods=(20, 30),
        ranking_metric=RankingMetric.WIN_RATE,
    )

    second = OptimizationConfig(
        fast_periods=(5, 9),
        slow_periods=(20, 30),
        ranking_metric=RankingMetric.WIN_RATE,
    )

    assert first == second


def main() -> None:

    test_valid_configuration()
    test_empty_fast_periods()
    test_empty_slow_periods()
    test_invalid_max_combinations()
    test_determinism()

    print("=" * 60)
    print(
        "Optimization Config Validation Passed"
    )
    print("=" * 60)
    print()
    print(
        "Configuration        : OK"
    )
    print(
        "Validation           : OK"
    )
    print(
        "Determinism          : OK"
    )
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()