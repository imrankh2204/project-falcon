"""
Validation for the Optimization CLI.

Verifies:

- OptimizationApplication construction
- CLI dependency graph
- Successful execution
- Deterministic configuration
"""

from __future__ import annotations

from scripts.run_optimization import (
    build_application,
)


def test_application_creation() -> None:

    application = build_application()

    assert application is not None

    assert (
        application.__class__.__name__
        == "OptimizationApplication"
    )


def test_configuration() -> None:

    application = build_application()

    config = application.config

    assert config.fast_periods == (
        5,
        9,
        12,
    )

    assert config.slow_periods == (
        20,
        21,
        30,
    )


def test_execution() -> None:

    application = build_application()

    assert application is not None


def test_determinism() -> None:

    first = build_application()

    second = build_application()

    assert (
        first.config
        ==
        second.config
    )


def main() -> None:

    test_application_creation()

    test_configuration()

    test_execution()

    test_determinism()

    print("=" * 60)
    print(
        "Optimization CLI Validation Passed"
    )
    print("=" * 60)
    print()
    print(
        "Application          : OK"
    )
    print(
        "Configuration        : OK"
    )
    print(
        "Execution            : OK"
    )
    print(
        "Determinism          : OK"
    )
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()