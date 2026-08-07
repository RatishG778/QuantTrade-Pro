from pathlib import Path
import sqlite3


class ResearchDatabase:

    def __init__(self):

        db_folder = Path("research/database")

        db_folder.mkdir(parents=True, exist_ok=True)

        self.db_path = db_folder / "research.db"

        self.connection = sqlite3.connect(self.db_path)

        self.create_tables()

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            created_at TEXT,

            strategy TEXT,

            symbol TEXT,

            capital REAL,

            parameters TEXT,

            profit REAL,

            return_pct REAL,

            sharpe REAL,

            max_drawdown REAL,

            trades INTEGER,

            win_rate REAL

        )
        """)

        self.connection.commit()