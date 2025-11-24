"""
Telemetry Engine orchestrates heartbeat, drift, and governance signals.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict

from configs.config_loader import load_config
from relay.notion_relay import NotionRelay
from relay.slack_signalbot import SlackSignalBot
from relay.teamwork_sink import TeamworkSink


@dataclass
class TelemetryRecord:
    signal_type: str
    payload: Dict[str, str]
    level: str = "info"


class TelemetryEngine:
    def __init__(self) -> None:
        config = load_config()
        self.thresholds = config.get("telemetry", {}).get("drift_thresholds", {})
        routes = config.get("telemetry", {}).get("routes", {})
        self.relays = {
            "slack": SlackSignalBot(routes.get("slack", "governance-telemetry")),
            "notion": NotionRelay(routes.get("notion", "activations-ledger")),
            "teamwork": TeamworkSink(routes.get("teamwork", "maos-evidence-room")),
        }

    def emit(self, record: TelemetryRecord) -> None:
        message = {
            "signal_type": record.signal_type,
            "level": record.level,
            "payload": record.payload,
            "ts": datetime.now(tz=timezone.utc).isoformat(),
        }
        for client in self.relays.values():
            client.send(record.signal_type, message)

    def emit_heartbeat(self, run_id: str, seal_version: str) -> None:
        payload = {
            "run_id": run_id,
            "seal_version": seal_version,
            "category": "heartbeat",
        }
        self.emit(TelemetryRecord(signal_type="heartbeat", payload=payload))

    def compute_drift_level(self, drift_score: int) -> str:
        green_max = self.thresholds.get("green_max", 10)
        yellow_max = self.thresholds.get("yellow_max", 30)

        if drift_score <= green_max:
            return "green"
        if drift_score <= yellow_max:
            return "yellow"
        return "red"

    def emit_drift(self, drift_score: int, correlation_id: str) -> str:
        level = self.compute_drift_level(drift_score)
        payload = {
            "drift_score": str(drift_score),
            "correlation_id": correlation_id,
            "category": "drift",
            "level": level,
        }
        self.emit(
            TelemetryRecord(
                signal_type="drift",
                payload=payload,
                level="warning" if level != "green" else "info",
            )
        )
        return level