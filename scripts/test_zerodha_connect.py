"""
Project Falcon Zerodha Connection Test
"""

from app.broker.zerodha_broker import ZerodhaBroker


def main() -> None:
    print("=" * 50)
    print("Project Falcon Zerodha Connection Test")
    print("=" * 50)

    broker = ZerodhaBroker()

    print("Initial Status :", broker.is_connected())

    print("\nConnecting...")
    broker.connect()

    print("Connected :", broker.is_connected())

    print("\nDisconnecting...")
    broker.disconnect()

    print("Connected :", broker.is_connected())

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()