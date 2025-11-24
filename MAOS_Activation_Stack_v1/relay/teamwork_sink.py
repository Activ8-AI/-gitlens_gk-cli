"""
Teamwork relay writing evidence and drift scores.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from relay.base import RelayClient


class TeamworkSink(RelayClient):
    def __init__(self, channel: str = "maos-evidence-room") -> None:
        super().__init__(channel)
        self._log_path = Path(__file__).parents[1] / ".runtime" / "teamwork_signals.log"
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

    def send(self, signal_type: str, payload: Dict[str, Any]) -> None:
        record = {
            "ts": datetime.now(tz=timezone.utc).isoformat(),
            "route": self.channel,
            "signal_type": signal_type,
            "payload": payload,
        }
        with self._log_path.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(record) + "\n")