"""
Project Falcon

FAL-590-R1

Runtime Persistence Service

Coordinates persistence of runtime session reports.

Responsibilities
----------------
- Validate runtime reports.
- Delegate persistence.
- Preserve Clean Architecture.
- Remain storage independent.

The service intentionally does NOT implement:

- SQLite
- JSON export
- File I/O
- ORM
"""

from __future__ import annotations

from app.live.runtime_repository import (
    RuntimeRepository,
)
from app.live.runtime_session_report import (
    RuntimeSessionReport,
)


class RuntimePersistenceService:
    """
    Application service responsible for persisting
    runtime session reports.
    """

    def __init__(
        self,
        *,
        repository: RuntimeRepository,
    ) -> None:

        self._repository = repository

    def persist(
        self,
        report: RuntimeSessionReport,
    ) -> RuntimeSessionReport:
        """
        Persist a runtime session report.
        """

        if not isinstance(
            report,
            RuntimeSessionReport,
        ):
            raise TypeError(
                "report must be a RuntimeSessionReport."
            )

        return self._repository.save(
            report,
        )