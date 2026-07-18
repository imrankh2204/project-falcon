"""
Project Falcon Zerodha Client Test
"""

from app.broker.zerodha_broker import ZerodhaBroker


def main() -> None:
    print("=" * 50)
    print("Project Falcon Zerodha Client Test")
    print("=" * 50)

    broker = ZerodhaBroker()

    print("Broker created successfully.")
    print(f"SDK Client : {type(broker.kite).__name__}")

    print()
    print("STATUS : PASS")


if __name__ == "__main__":
    main()