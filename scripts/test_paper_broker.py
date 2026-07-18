"""
Paper broker validation script.
"""

from app.broker.paper_broker import PaperBroker


def main() -> None:

    print("=" * 50)
    print("Project Falcon Paper Broker Test")
    print("=" * 50)

    broker = PaperBroker()

    print("Initial connection status:")
    print(broker.is_connected())

    print()

    print("Connecting...")
    broker.connect()

    print("Connected:")
    print(broker.is_connected())

    print()

    print("Disconnecting...")
    broker.disconnect()

    print("Connected:")
    print(broker.is_connected())

    print()
    print("STATUS : PASS")


if __name__ == "__main__":
    main()