"""
Placeholder for Slack signal relay.
"""

from __future__ import annotations

from typing import Dict


def notify_slack(payload: Dict[str, str]) -> Dict[str, str]:
    return {"channel": "slack", **payload}


__all__ = ["notify_slack"]
