"""
Application bootstrap validation.
"""

from app.core.application import Application


def main() -> None:

    print("=" * 50)
    print("Project Falcon Application Test")
    print("=" * 50)

    app = Application()

    print("Starting application...")
    app.start()

    print("Application started successfully.")

    print("Shutting down...")
    app.shutdown()

    print("Application shutdown successfully.")
    print()
    print("STATUS : PASS")


if __name__ == "__main__":
    main()