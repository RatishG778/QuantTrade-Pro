from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResearchNote:

    experiment_id: int

    strategy: str

    title: str

    observation: str

    lesson: str

    next_step: str

    created_at: datetime