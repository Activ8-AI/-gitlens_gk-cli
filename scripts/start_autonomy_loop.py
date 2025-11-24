#!/usr/bin/env python3
"""
Simple autonomy loop that emits ledger entries.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_hub.activate import activate_agent
from custody.custodian_ledger import record_event


def run_loop(iterations: int, sleep_seconds: float) -> None:
    for idx in range(iterations):
        activation_payload = activate_agent(idx)
        record_event("AUTONOMY_LOOP", activation_payload)
        print(f"[loop] recorded AUTONOMY_LOOP payload {activation_payload}")
        time.sleep(sleep_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the autonomy loop.")
    parser.add_argument("--iterations", type=int, default=3, help="Number of loop iterations")
    parser.add_argument("--sleep", type=float, default=0.5, help="Seconds to wait between iterations")
    args = parser.parse_args()
    run_loop(args.iterations, args.sleep)


if __name__ == "__main__":
    main()
