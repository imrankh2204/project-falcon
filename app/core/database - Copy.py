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

    def initialize_schema(self) -> None:
        """
        Initialize the SQLite database using schema.sql.
        """
        
        if self.connection is None:
            raise RuntimeError("Database connection is not established.")

    try:
        self.logger.info("Loading schema.sql...")

        schema_path = Path("database") / "schema.sql"

        if not schema_path.exists():
            raise FileNotFoundError(
                f"Schema file not found: {schema_path}"
            )

        with open(schema_path, "r", encoding="utf-8") as file:
            schema = file.read()

        self.connection.executescript(schema)

        self.connection.commit()

        self.logger.info(
            "Database schema initialized successfully."
        )

    except Exception:
        self.logger.exception(
            "Failed to initialize database schema."
        )
        raise
    
    def verify_schema(self) -> bool:
        """
        Verify that all required tables exist.
        """

    if self.connection is None:
        return False

    required_tables = {
        "application_state",
        "application_events",
        "market_sessions",
        "paper_trades",
    }

    cursor = self.connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table';
        """
    )

    tables = {row[0] for row in cursor.fetchall()}

    missing = required_tables - tables

    if missing:
        self.logger.error(
            "Missing database tables: %s",
            ", ".join(sorted(missing)),
        )
        return False

    self.logger.info(
        "Verified required database tables."
    )

    return True

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
    
    def close(self) -> None:
        """
        Close SQLite connection.
        """

        if self.connection is not None:
            self.logger.info("Closing database connection...")

            self.connection.close()

            self.connection = None

            self.logger.info("Database connection closed.")

    def execute(self, query: str, parameters: tuple = ()) -> None:
        """
        Placeholder for FAL-012C.
        """
        raise NotImplementedError(
            "execute() will be implemented during FAL-012C."
        )
