"""
Placeholder for Notion relay interactions.
"""

from __future__ import annotations

from typing import Dict


def send_to_notion(payload: Dict[str, str]) -> Dict[str, str]:
    return {"channel": "notion", **payload}


__all__ = ["send_to_notion"]
