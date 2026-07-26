"""
Walk-forward optimization validation for Project Falcon.

Validates:
- Configuration creation.
- Window validation.
- Result construction.
- Engine execution.
- Service orchestration.
- Deterministic behaviour.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.backtest.optimization.result import (
    OptimizationResult,
)

from app.backtest.walk_forward.config import (
    WalkForwardConfig,
)

from app.backtest.walk_forward.engine import (
    WalkForwardEngine,
)

from app.backtest.walk_forward.result import (
    WalkForwardResult,
)

from app.backtest.walk_forward.service import (
    WalkForwardService,
)

from app.backtest.walk_forward.window import (
    WalkForwardWindow,
)

from app.strategies.ema_parameters import (
    EMACrossoverParameters,
)


class DummyOptimizationService:
    """
    Deterministic optimization service stub.
    """

    def run(
        self,
        _window,
    ):
        return OptimizationResult(
            parameters=EMACrossoverParameters(
                fast_period=5,
                slow_period=20,
            ),
            report=None,
        )


class DummyBacktestFactory:
    """
    Deterministic backtest factory stub.
    """

    def create(
        self,
        _strategy,
    ):
        """
        Return a deterministic application stub.
        """

        return None


def build_engine() -> WalkForwardEngine:

    return WalkForwardEngine(
        optimization_service=DummyOptimizationService(),
        backtest_factory=DummyBacktestFactory(),
    )


def build_window() -> WalkForwardWindow:

    return WalkForwardWindow(
        training_start=datetime(
            2026,
            1,
            1,
            tzinfo=timezone.utc,
        ),
        training_end=datetime(
            2026,
            3,
            1,
            tzinfo=timezone.utc,
        ),
        validation_start=datetime(
            2026,
            3,
            1,
            tzinfo=timezone.utc,
        ),
        validation_end=datetime(
            2026,
            3,
            20,
            tzinfo=timezone.utc,
        ),
    )


def test_configuration() -> None:

    config = WalkForwardConfig(
        training_days=60,
        validation_days=20,
        step_days=20,
    )

    assert config.training_days == 60


def test_window() -> None:

    window = build_window()

    assert (
        window.training_duration_days
        ==
        59
    )

    assert (
        window.validation_duration_days
        ==
        19
    )


def test_engine_execution() -> None:

    engine = build_engine()

    result = engine.run(
        windows=[
            build_window()
        ]
    )

    assert isinstance(
        result,
        WalkForwardResult,
    )

    assert (
        result.iteration_count
        ==
        1
    )


def test_service_execution() -> None:

    service = WalkForwardService(
        engine=build_engine()
    )

    result = service.run(
        config=WalkForwardConfig(
            training_days=60,
            validation_days=20,
            step_days=20,
        ),
        windows=[
            build_window()
        ],
    )

    assert (
        result.iteration_count
        ==
        1
    )


def test_determinism() -> None:

    engine = build_engine()

    first = engine.run(
        windows=[
            build_window()
        ]
    )

    second = engine.run(
        windows=[
            build_window()
        ]
    )

    assert first == second


def main() -> None:

    test_configuration()
    test_window()
    test_engine_execution()
    test_service_execution()
    test_determinism()

    print("=" * 60)
    print(
        "Walk-Forward Validation Passed"
    )
    print("=" * 60)
    print()
    print(
        "Configuration   : OK"
    )
    print(
        "Window          : OK"
    )
    print(
        "Engine          : OK"
    )
    print(
        "Service         : OK"
    )
    print(
        "Determinism     : OK"
    )
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()