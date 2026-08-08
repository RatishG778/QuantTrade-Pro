from dataclasses import dataclass
from datetime import datetime


@dataclass
class AutomationJob:

    symbol: str

    strategy: str

    status: str = "Pending"

    started_at: datetime | None = None

    finished_at: datetime | None = None

    error: str | None = None