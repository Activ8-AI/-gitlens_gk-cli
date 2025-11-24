"""
Trivial in-memory vector store stub.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class VectorMemory:
    key: str
    vector: List[float]
    metadata: Dict[str, str] = field(default_factory=dict)


class VectorStore:
    def __init__(self):
        self._storage: Dict[str, VectorMemory] = {}

    def upsert(self, memory: VectorMemory) -> None:
        self._storage[memory.key] = memory

    def fetch(self, key: str) -> VectorMemory | None:
        return self._storage.get(key)

    def all_keys(self) -> List[str]:
        return list(self._storage.keys())


__all__ = ["VectorStore", "VectorMemory"]
