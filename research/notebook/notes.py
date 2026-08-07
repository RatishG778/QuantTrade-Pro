from dataclasses import dataclass


@dataclass
class ResearchNote:

    experiment_id: int

    title: str

    observation: str

    weakness: str

    next_step: str
    