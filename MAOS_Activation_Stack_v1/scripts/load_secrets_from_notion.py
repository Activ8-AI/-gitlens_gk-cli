"""
Loads secrets from Notion (or local fallback) and stages them for runtime.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Optional

class SecretLoader:
    def __init__(self, fallback_env: str = "NOTION_SECRETS") -> None:
        self.fallback_env = fallback_env
        self.runtime_path = Path(__file__).parents[1] / ".runtime" / "secrets.json"
        self.runtime_path.parent.mkdir(parents=True, exist_ok=True)
        self.source_file = Path(__file__).parents[1] / "configs" / "secrets.json"

    def _read_source(self) -> Optional[Dict[str, str]]:
        if self.source_file.exists():
            with self.source_file.open("r", encoding="utf-8") as fp:
                return json.load(fp)
        raw_env = os.getenv(self.fallback_env)
        if raw_env:
            return json.loads(raw_env)
        return None

    def load(self) -> Dict[str, str]:
        secrets = self._read_source()
        if not secrets:
            raise RuntimeError(
                "No secrets detected. Provide configs/secrets.json or set NOTION_SECRETS."
            )
        with self.runtime_path.open("w", encoding="utf-8") as fp:
            json.dump(secrets, fp, indent=2)
        return secrets


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load charter-governed secrets for MAOS Activation Stack."
    )
    parser.add_argument(
        "--echo",
        action="store_true",
        help="Print the detected secrets (values redacted) for verification.",
    )
    args = parser.parse_args()

    loader = SecretLoader()
    secrets = loader.load()

    if args.echo:
        redacted = {key: "***" for key in secrets}
        print(json.dumps(redacted, indent=2))


if __name__ == "__main__":
    main()