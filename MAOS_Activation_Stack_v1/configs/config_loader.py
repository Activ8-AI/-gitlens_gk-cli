"""
Lightweight helper for loading the canonical MAOS configuration once per process.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

try:
    import yaml  # type: ignore
except ImportError as exc:  # pragma: no cover - explicit guidance for operators
    raise RuntimeError(
        "PyYAML is required to load the MAOS global configuration. "
        "Install it with `pip install pyyaml` before booting the stack."
    ) from exc


CONFIG_PATH = Path(__file__).with_name("global_config.yaml")


@lru_cache(maxsize=1)
def load_config() -> Dict[str, Any]:
    """
    Loads the canonical config.yaml and memoizes the content to keep access cheap.
    """
    with CONFIG_PATH.open("r", encoding="utf-8") as fp:
        return yaml.safe_load(fp) or {}


def get_path(key: str) -> Path:
    """
    Resolve configured relative paths from the repository root.
    """
    config = load_config()
    base = Path(config.get("paths", {}).get("core_root", CONFIG_PATH.parents[1]))
    relative = config.get("paths", {}).get(key)
    if not relative:
        raise KeyError(f"Unknown path key '{key}' in configuration.")
    return (base / relative).resolve()
