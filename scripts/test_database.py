"""
Database validation script.
"""

from app.core.database import DatabaseManager

def main() -> None:

    print("=" * 50)
    print("Project Falcon Database Test")
    print("=" * 50)

    db = DatabaseManager()

    print("Opening database...")
    db.connect()

    print("Initializing schema...")
    db.initialize_schema()

    print("Schema initialized.")

    print("Verifying schema...")
    assert db.verify_schema()

    print("Schema verification PASSED")

    print("Running health check...")
    assert db.health_check()

    print("Health check PASSED")

    db.close()

    print("Connection closed")
    print()

    print("STATUS : PASS")


if __name__ == "__main__":
    main()