#!/usr/bin/env python3
"""
Stub script that pretends to load secrets from Notion.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from telemetry.emit_heartbeat import load_config


def fake_fetch_from_notion(config: Dict[str, Any]) -> Dict[str, str]:
    notion_meta = config.get("notion", {})
    return {
        "NOTION_DATABASE_ID": notion_meta.get("database_id", "missing"),
        "NOTION_SECRET_KEY": notion_meta.get("secret_key", "missing"),
    }


def main() -> None:
    config = load_config()
    secrets = fake_fetch_from_notion(config)
    secrets_path = Path("configs/.secrets_cache.json")
    secrets_path.write_text(json.dumps(secrets, indent=2), encoding="utf-8")
    print(f"Stored {len(secrets)} secrets at {secrets_path}")


if __name__ == "__main__":
    main()
