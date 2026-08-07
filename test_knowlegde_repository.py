from datetime import datetime

from knowledge.note import ResearchNote
from knowledge.repository import KnowledgeRepository

repo = KnowledgeRepository()

repo.save(

    ResearchNote(

        experiment_id=1,

        strategy="Moving Average",

        title="First Success",

        observation="Worked well in trending market.",

        lesson="Avoid sideways market.",

        next_step="Test with ADX filter.",

        created_at=datetime.now()

    )

)