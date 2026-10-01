from __future__ import annotations

import sqlite3
from typing import Any


class StrategyRepository:
    def __init__(self, db_path: str = "quanttrade_pro.db") -> None:
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._initialize()

    def _initialize(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS strategies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                version TEXT NOT NULL,
                environment TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.connection.commit()

    def save(self, strategy: dict[str, Any]) -> dict[str, Any]:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO strategies (id, name, description, version, environment, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                strategy["id"],
                strategy["name"],
                strategy.get("description", ""),
                strategy["version"],
                strategy["environment"],
                strategy.get("status", "draft"),
            ),
        )
        self.connection.commit()
        return strategy

    def list(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT id, name, description, version, environment, status, created_at FROM strategies ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_by_id(self, strategy_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT id, name, description, version, environment, status, created_at FROM strategies WHERE id = ?",
            (strategy_id,),
        ).fetchone()
        if row is None:
            return None
        return dict(row)
