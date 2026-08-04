from dataclasses import dataclass


@dataclass
class Trade:

    entry_date: str
    exit_date: str

    entry_price: float
    exit_price: float

    quantity: int

    side: str

    profit: float = 0.0