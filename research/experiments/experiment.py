from dataclasses import dataclass
from datetime import datetime


@dataclass
class Experiment:

    name: str

    strategy: str

    symbol: str

    capital: float

    parameters: dict

    created_at: datetime = datetime.now()