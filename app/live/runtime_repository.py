"""
Project Falcon

FAL-590-R2

Runtime Repository Contract

Defines the persistence contract for runtime session reports.

Responsibilities
----------------
- Define the persistence interface.
- Preserve dependency inversion.
- Remain storage independent.

The contract intentionally does NOT implement:

- SQLite
- JSON
- File I/O
- ORM
"""

from __future__ import annotations

from typing import Protocol

from app.live.runtime_session_report import (
    RuntimeSessionReport,
)


class RuntimeRepository(Protocol):
    """
    Persistence contract for runtime session reports.
    """

    def save(
        self,
        report: RuntimeSessionReport,
    ) -> RuntimeSessionReport:
        """
        Persist a runtime session report.

        Returns
        -------
        RuntimeSessionReport
            The persisted report.
        """
        ...