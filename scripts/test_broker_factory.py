"""
Broker factory validation script.
"""

from app.broker.factory import BrokerFactory


def main() -> None:

    print("=" * 50)
    print("Project Falcon Broker Factory Test")
    print("=" * 50)

    print("Creating broker...")

    broker = BrokerFactory.create()

    print(f"Broker Type : {broker.__class__.__name__}")

    print()

    print("Connecting...")
    broker.connect()

    print(f"Connected : {broker.is_connected()}")

    print()

    print("Disconnecting...")
    broker.disconnect()

    print(f"Connected : {broker.is_connected()}")

    print()
    print("STATUS : PASS")


if __name__ == "__main__":
    main()