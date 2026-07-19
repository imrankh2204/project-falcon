"""
Project Falcon Strategy Interface Test
"""

from app.strategies.strategy import Strategy


class DummyStrategy(Strategy):
    @property
    def name(self) -> str:
        return "Dummy Strategy"

    def evaluate(self, candles):
        return None


def main() -> None:
    print("=" * 50)
    print("Project Falcon Strategy Test")
    print("=" * 50)

    strategy = DummyStrategy()

    print(f"Strategy : {strategy.name}")

    assert strategy.name == "Dummy Strategy"

    print("\nSTATUS : PASS")


if __name__ == "__main__":
    main()