"""
Custodian Ledger - append-only governance ledger backed by SQLite.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from configs.config_loader import get_path


@dataclass
class LedgerEvent:
    event_type: str
    actor_identity: str
    payload: Dict[str, Any]
    correlation_id: str
    seal_version: str
    environment: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(tz=timezone.utc).isoformat()
    )


class CustodianLedger:
    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = Path(db_path or get_path("custody_ledger"))
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    actor_identity TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    correlation_id TEXT NOT NULL,
                    seal_version TEXT NOT NULL,
                    environment TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def write_event(self, event: LedgerEvent) -> int:
        serialized_payload = json.dumps(event.payload, sort_keys=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO ledger (
                    timestamp, event_type, actor_identity, payload,
                    correlation_id, seal_version, environment
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.timestamp,
                    event.event_type,
                    event.actor_identity,
                    serialized_payload,
                    event.correlation_id,
                    event.seal_version,
                    event.environment,
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def recent_events(self, limit: int = 25) -> Iterable[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM ledger ORDER BY id DESC LIMIT ?", (limit,)
            )
            for row in cursor:
                yield {
                    "id": row["id"],
                    "timestamp": row["timestamp"],
                    "event_type": row["event_type"],
                    "actor_identity": row["actor_identity"],
                    "payload": json.loads(row["payload"]),
                    "correlation_id": row["correlation_id"],
                    "seal_version": row["seal_version"],
                    "environment": row["environment"],
                }
