"""
Placeholder for Teamwork sink relay.
"""

from __future__ import annotations

from typing import Dict


def notify_teamwork(payload: Dict[str, str]) -> Dict[str, str]:
    return {"channel": "teamwork", **payload}


__all__ = ["notify_teamwork"]
