"""
Database management for Project Falcon.

Provides a lightweight wrapper around SQLite.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from app.core.logger import get_logger


class DatabaseManager:
    """
    Handles SQLite connection management.
    """

    def __init__(self) -> None:
        self.logger = get_logger("database")

        self.database_directory = Path("data") / "database"

        self.database_path = self.database_directory / "falcon.db"

        self.connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        """
        Open a SQLite connection.
        """

        try:
            self.logger.info("Verifying database directory...")

            self.database_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            self.logger.info("Opening SQLite database...")

            self.connection = sqlite3.connect(self.database_path)

            self.logger.info("SQLite connection established.")

            return self.connection

        except Exception:
            self.logger.exception(
                "Failed to establish database connection."
            )
            raise

    def close(self) -> None:
        """
        Close SQLite connection.
        """

        if self.connection is not None:
            self.logger.info("Closing database connection...")

            self.connection.close()

            self.connection = None

            self.logger.info("Database connection closed.")

    def health_check(self) -> bool:
        """
        Simple connectivity test.

        Executes:

            SELECT 1;
        """

        try:
            if self.connection is None:
                return False

            cursor = self.connection.cursor()

            cursor.execute("SELECT 1;")

            cursor.fetchone()

            return True

        except Exception:
            self.logger.exception(
                "Database health check failed."
            )

            return False