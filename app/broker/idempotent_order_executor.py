"""
Idempotent order execution helper.

Ensures that a logical broker operation is executed at most once for
a given idempotency key.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")


class IdempotentOrderExecutor(Generic[T]):
    """
    Executes broker operations with simple idempotency guarantees.
    """

    def __init__(self) -> None:
        self._completed: dict[str, T] = {}

    def execute(
        self,
        *,
        key: str,
        operation: Callable[[], T],
    ) -> T:
        """
        Execute an operation once for the supplied key.
        """

        if not isinstance(key, str):
            raise TypeError("key must be a string.")

        if not key.strip():
            raise ValueError("key cannot be empty.")

        if key in self._completed:
            return self._completed[key]

        result = operation()

        self._completed[key] = result

        return result

    def clear(self) -> None:
        """
        Clear cached execution history.
        """

        self._completed.clear()