"""
FastAPI relay server exposing health + heartbeat endpoints.
"""

from __future__ import annotations

from pathlib import Path
import sys

from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from custody.custodian_ledger import get_recent_events
from telemetry.emit_heartbeat import emit_heartbeat, load_config

app = FastAPI(title="Core Pack MCP Relay")


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/heartbeat")
def heartbeat() -> dict:
    return emit_heartbeat()


@app.get("/ledger")
def ledger_tail(limit: int = 5) -> dict:
    return {"events": list(get_recent_events("AUTONOMY_LOOP", limit=limit))}


def _server_kwargs() -> dict:
    config = load_config()
    mcp_cfg = config.get("mcp", {})
    return {"host": mcp_cfg.get("host", "0.0.0.0"), "port": mcp_cfg.get("port", 8000)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("orchestration.MCP.relay_server:app", **_server_kwargs(), reload=False)
