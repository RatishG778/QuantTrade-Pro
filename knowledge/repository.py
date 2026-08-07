import json
from pathlib import Path
from dataclasses import asdict
from datetime import datetime

from knowledge.note import ResearchNote


class KnowledgeRepository:

    def __init__(self):

        self.file = Path("knowledge.json")

    def save(self, note: ResearchNote):

        data = []

        if self.file.exists():

            data = json.loads(

                self.file.read_text()

            )

        item = asdict(note)

        item["created_at"] = item["created_at"].isoformat()

        data.append(item)

        self.file.write_text(

            json.dumps(

                data,

                indent=4

            )

        )