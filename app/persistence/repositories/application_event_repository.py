"""
Base repository implementation for Project Falcon.

All repository classes should inherit from BaseRepository to gain
access to the shared DatabaseManager instance and common persistence
operations.
"""

from __future__ import annotations

from app.core.database import DatabaseManager


class BaseRepository:
    """
    Base class for all Falcon repositories.

    This class provides a common database interface for higher-level
    repositories such as TradeRepository, PositionRepository,
    MarketDataRepository, and ApplicationEventRepository.
    """

    def __init__(self, database: DatabaseManager) -> None:
        """
        Initialize the repository.

        Parameters
        ----------
        database
            Active DatabaseManager instance.
        """
        self.database = database

    @property
    def connection(self):
        """
        Return the active SQLite connection.

        This property is intentionally read-only.
        """
        return self.database.connection

    def health_check(self) -> bool:
        """
        Delegate the database health check.

        Returns
        -------
        bool
            True if the database is healthy.
        """
        return self.database.health_check()