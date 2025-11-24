"""
Common relay interface for telemetry and evidence sinks.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class RelayClient(ABC):
    def __init__(self, channel: str) -> None:
        self.channel = channel

    @abstractmethod
    def send(self, signal_type: str, payload: Dict[str, Any]) -> None:
        """Send a signal to the downstream system."""
