from __future__ import annotations

import sqlite3

DEFAULT_DB_PATH = "quanttrade_pro.db"


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection
