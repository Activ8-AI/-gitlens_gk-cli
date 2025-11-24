"""
Agent activation stub used by the autonomy loop.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict


def activate_agent(task_id: int) -> Dict[str, str]:
    return {
        "task_id": str(task_id),
        "intent": "stabilize_core_pack",
        "activated_at": datetime.now(timezone.utc).isoformat(),
    }


__all__ = ["activate_agent"]
