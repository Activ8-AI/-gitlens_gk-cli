"""
Vector-like memory pack implemented via lightweight JSON persistence.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable, List

from configs.config_loader import get_path


@dataclass
class MemoryFragment:
    text: str
    tags: List[str]
    importance: int = 1


class MemoryPack:
    def __init__(self, filename: str = "memory_pack.json") -> None:
        directory = get_path("memory_vector_store")
        directory.mkdir(parents=True, exist_ok=True)
        self.file_path = directory / filename
        self._fragments: List[MemoryFragment] = []
        self._load()

    def _load(self) -> None:
        if not self.file_path.exists():
            return
        with self.file_path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
            self._fragments = [
                MemoryFragment(**fragment) for fragment in data.get("fragments", [])
            ]

    def _persist(self) -> None:
        serialized = {
            "fragments": [
                {"text": frag.text, "tags": frag.tags, "importance": frag.importance}
                for frag in self._fragments
            ]
        }
        with self.file_path.open("w", encoding="utf-8") as fp:
            json.dump(serialized, fp, indent=2)

    def add_memory(self, fragment: MemoryFragment) -> None:
        self._fragments.append(fragment)
        self._persist()

    def search(self, keyword: str) -> Iterable[MemoryFragment]:
        keyword_lower = keyword.lower()
        yield from (
            fragment
            for fragment in self._fragments
            if keyword_lower in fragment.text.lower()
            or keyword_lower in " ".join(fragment.tags).lower()
        )
