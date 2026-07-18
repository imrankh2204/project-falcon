"""
Project Falcon Zerodha Offline Validation
"""

from app.broker.exceptions import BrokerAuthenticationError
from app.broker.zerodha_broker import ZerodhaBroker


def main() -> None:
    print("=" * 50)
    print("Project Falcon Zerodha Offline Test")
    print("=" * 50)

    broker = ZerodhaBroker()

    print("Broker instantiated successfully.")
    print("Connected :", broker.is_connected())

    print("\nAttempting initialization...")

    try:
        broker.connect()

        print("Initialization succeeded.")
        print("Connected :", broker.is_connected())

    except BrokerAuthenticationError as exc:
        print("Expected authentication exception:")
        print(exc)

    print("\nDisconnecting...")
    broker.disconnect()

    print("Connected :", broker.is_connected())

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()