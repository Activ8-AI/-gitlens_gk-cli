"""
Telemetry helpers for heartbeat emissions.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

CONFIG_PATH = Path(__file__).resolve().parent.parent / "configs" / "global_config.yaml"


def _default_config() -> Dict[str, Any]:
    return {
        "environment": "development",
        "telemetry": {"heartbeat_interval_seconds": 5},
    }


def load_config() -> Dict[str, Any]:
    """
    Load the YAML config if PyYAML is available, otherwise use defaults.
    """
    if not CONFIG_PATH.exists():
        return _default_config()

    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:
        return _default_config()

    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or _default_config()


def emit_heartbeat() -> Dict[str, Any]:
    """
    Build a simple heartbeat payload for the API.
    """
    config = load_config()
    heartbeat_meta = config.get("telemetry", {})
    return {
        "status": "alive",
        "environment": config.get("environment", "development"),
        "heartbeat_interval_seconds": heartbeat_meta.get("heartbeat_interval_seconds", 5),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


__all__ = ["emit_heartbeat", "load_config"]
