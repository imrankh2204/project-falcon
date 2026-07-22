from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PortfolioPerformance:

    total_realized_pnl: float

    closed_position_count: int
    winning_position_count: int
    losing_position_count: int
    breakeven_position_count: int

    win_rate: float

    average_winning_pnl: float
    average_losing_pnl: float

    profit_factor: float

    expectancy: float