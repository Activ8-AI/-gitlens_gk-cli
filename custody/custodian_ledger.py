"""
Simple ledger utilities backed by SQLite for tracking automation events.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, List

from telemetry.emit_heartbeat import load_config


class CustodianLedger:
    """
    Lightweight wrapper around a SQLite ledger.
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ledger_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def record(self, channel: str, payload: Dict[str, Any]) -> None:
        """
        Insert a new ledger row.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO ledger_entries (channel, payload) VALUES (?, ?)",
                (channel, json.dumps(payload)),
            )
            conn.commit()

    def tail(self, channel: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Return the last N rows for a given channel.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT payload, created_at
                FROM ledger_entries
                WHERE channel = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (channel, limit),
            )
            rows = cursor.fetchall()

        entries: List[Dict[str, Any]] = []
        for payload_json, created_at in rows:
            try:
                payload_data = json.loads(payload_json)
            except json.JSONDecodeError:
                payload_data = {"raw": payload_json}
            payload_data["created_at"] = created_at
            entries.append(payload_data)
        return entries


def get_ledger() -> CustodianLedger:
    """
    Resolve ledger location from config.
    """
    config = load_config()
    ledger_path = config.get("custody", {}).get("ledger_path", "custody/ledger.db")
    return CustodianLedger(Path(ledger_path))


def record_event(channel: str, payload: Dict[str, Any]) -> None:
    get_ledger().record(channel, payload)


def get_recent_events(channel: str, limit: int = 5) -> Iterable[Dict[str, Any]]:
    return get_ledger().tail(channel, limit)


__all__ = ["CustodianLedger", "get_ledger", "record_event", "get_recent_events"]
