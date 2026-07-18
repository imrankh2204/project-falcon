"""
Application bootstrap for Project Falcon.

Coordinates startup and shutdown of the application's
core infrastructure components.
"""

from __future__ import annotations

from app.core.database import DatabaseManager
from app.core.logger import get_logger


class Application:
    """
    Coordinates Falcon startup and shutdown.
    """

    def __init__(self) -> None:
        self.logger = get_logger("application")
        self.database = DatabaseManager()

    def start(self) -> None:
        """
        Start the application.
        """

        self.logger.info("Starting Project Falcon...")

        self.database.connect()
        self.database.initialize_schema()
        self.database.verify_schema()

        if not self.database.health_check():
            raise RuntimeError("Database health check failed.")

        self.logger.info("Project Falcon started successfully.")

    def shutdown(self) -> None:
        """
        Shutdown the application.
        """

        self.logger.info("Shutting down Project Falcon...")

        self.database.close()

        self.logger.info("Shutdown complete.")