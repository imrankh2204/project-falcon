"""
Health monitoring for Project Falcon.

Provides infrastructure readiness checks that can be
extended as new subsystems are introduced.
"""

from __future__ import annotations

from typing import Any

from app.core.database import DatabaseManager
from app.core.logger import get_logger


class HealthMonitor:
    """
    Performs health checks for Falcon infrastructure.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.logger = get_logger("health")
        self.database = database

    def run(self) -> dict[str, Any]:
        """
        Execute all currently supported health checks.
        """

        results: dict[str, Any] = {}

        # Database connectivity
        database_ok = self.database.health_check()

        results["database"] = {
            "status": "PASS" if database_ok else "FAIL",
            "message": (
                "Database connection healthy."
                if database_ok
                else "Database health check failed."
            ),
        }

        overall = all(
            item["status"] == "PASS"
            for item in results.values()
        )

        results["overall"] = {
            "status": "READY" if overall else "NOT READY",
        }

        self.logger.info(
            "Health check completed: %s",
            results["overall"]["status"],
        )

        return results

    def is_ready(self) -> bool:
        """
        Return True when the application is ready.

        This is a convenience wrapper around run()
        for callers that only need a boolean result.
        """

        return self.run()["overall"]["status"] == "READY"