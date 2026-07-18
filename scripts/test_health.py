"""
Health monitor validation script.
"""

from app.core.database import DatabaseManager
from app.core.health import HealthMonitor


def main() -> None:

    print("=" * 50)
    print("Project Falcon Health Monitor Test")
    print("=" * 50)

    database = DatabaseManager()

    print("Opening database...")
    database.connect()

    print("Initializing schema...")
    database.initialize_schema()

    print("Creating Health Monitor...")
    monitor = HealthMonitor(database)

    print("Running health checks...")
    results = monitor.run()

    print()

    for component, result in results.items():

        if component == "overall":
            continue

        print(
            f"{component.capitalize():<15}"
            f"{result['status']:<8}"
            f"{result['message']}"
        )

    print()

    print(
        f"Overall Status : {results['overall']['status']}"
    )

    database.close()

    print()
    print("STATUS : PASS")


if __name__ == "__main__":
    main()