"""
Structured SQL memory store for deterministic data capture.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict, Optional

from configs.config_loader import get_path


class SqlMemoryStore:
    def __init__(self, db_name: str = "memory.db") -> None:
        directory = get_path("memory_sql_store")
        directory.mkdir(parents=True, exist_ok=True)
        self.db_path = directory / db_name
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_key TEXT NOT NULL UNIQUE,
                    payload TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def upsert(self, key: str, payload: Dict[str, Any]) -> None:
        encoded = json.dumps(payload, sort_keys=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO memories (memory_key, payload)
                VALUES (?, ?)
                ON CONFLICT(memory_key) DO UPDATE SET payload=excluded.payload
                """,
                (key, encoded),
            )
            conn.commit()

    def fetch(self, key: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT payload FROM memories WHERE memory_key = ?", (key,)
            )
            row = cursor.fetchone()
            return json.loads(row["payload"]) if row else None
