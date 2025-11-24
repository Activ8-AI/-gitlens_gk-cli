"""
Minimal SQL store wrapper used by the autonomy loop.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple


class SQLStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def execute(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(query, params)
            conn.commit()

    def fetchall(self, query: str, params: Tuple[Any, ...] = ()) -> Iterable[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            for row in cursor.fetchall():
                yield dict(row)


def get_default_store() -> SQLStore:
    return SQLStore(Path("memory/sql_store/state.db"))


__all__ = ["SQLStore", "get_default_store"]
