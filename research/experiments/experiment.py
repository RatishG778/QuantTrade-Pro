from dataclasses import dataclass
from datetime import datetime


@dataclass
class Experiment:

    strategy: str

    symbol: str

    capital: float

    parameters: dict

    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")