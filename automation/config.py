from dataclasses import dataclass


@dataclass
class AutomationConfig:

    symbols: list[str]

    strategies: list[str]

    capital: float = 100000

    optimize: bool = False

    validate: bool = False

    monte_carlo: bool = False

    portfolio_analysis: bool = False

    generate_report: bool = False