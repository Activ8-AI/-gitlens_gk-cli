"""
MCP Relay Server - stitches together telemetry, memory, ledger, and agents.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict

from agent_hub.activate import AgentHub
from configs.config_loader import get_path, load_config
from custody.ledger import CustodianLedger, LedgerEvent
from memory.sql_store.store import SqlMemoryStore
from memory.vector_store.memory_pack import MemoryFragment, MemoryPack
from scripts.load_secrets_from_notion import SecretLoader
from telemetry.telemetry_engine import TelemetryEngine


@dataclass
class ActivationState:
    run_id: str
    environment: str
    seal_version: str = "MVP_v0"
    checklist: Dict[str, bool] = field(default_factory=dict)


class MCPRelayServer:
    def __init__(self) -> None:
        self.config = load_config()
        self.ledger = CustodianLedger()
        self.telemetry = TelemetryEngine()
        self.sql_memory = SqlMemoryStore()
        self.memory_pack = MemoryPack()
        self.secret_loader = SecretLoader()
        self.agent_hub = AgentHub(self.ledger, self.telemetry)
        self.activation_sequence = self.config.get("activation_sequence", [])

    def _build_run_id(self) -> str:
        prefix = self.config.get("traceability", {}).get("run_prefix", "MAOS")
        return f"{prefix}-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"

    def verify_core_pack(self) -> None:
        required_paths = [
            get_path("memory_sql_store"),
            get_path("memory_vector_store"),
            get_path("custody_ledger"),
        ]
        missing = [str(path) for path in required_paths if not Path(path).exists()]
        if missing:
            raise FileNotFoundError(f"Core Pack verification failed. Missing: {missing}")

    def install_dependencies(self) -> None:
        # Placeholder for environment-specific setup hooks.
        self.sql_memory.upsert(
            "dependencies",
            {"status": "installed", "ts": datetime.utcnow().isoformat()},
        )

    def load_secrets(self) -> None:
        self.secret_loader.load()

    def emit_heartbeat(self, state: ActivationState) -> None:
        self.telemetry.emit_heartbeat(state.run_id, state.seal_version)

    def activate_agents(self, state: ActivationState) -> None:
        self.agent_hub.activate_agents(state.run_id, state.environment)

    def start_autonomy_loop(self, state: ActivationState) -> None:
        from autonomy.start_autonomy_loop import AutonomyLoop

        loop = AutonomyLoop(self.ledger, self.telemetry, self.memory_pack)
        loop.run_once(state.run_id, state.environment)

    def seal_mvp(self, state: ActivationState) -> None:
        self.ledger.write_event(
            LedgerEvent(
                event_type="seal",
                actor_identity="governance",
                payload={"seal_version": state.seal_version},
                correlation_id=state.run_id,
                seal_version=state.seal_version,
                environment=state.environment,
            )
        )

    def run_activation(self, environment: str = "dev") -> ActivationState:
        state = ActivationState(
            run_id=self._build_run_id(),
            environment=environment,
            checklist={step: False for step in self.activation_sequence},
        )

        actions = {
            "verify_core_pack": self.verify_core_pack,
            "install_dependencies": self.install_dependencies,
            "load_secrets": self.load_secrets,
            "start_mcp": lambda: self.sql_memory.upsert(
                "mcp_status", {"status": "online"}
            ),
            "emit_heartbeat": lambda: self.emit_heartbeat(state),
            "activate_agents": lambda: self.activate_agents(state),
            "start_autonomy_loop": lambda: self.start_autonomy_loop(state),
            "seal_mvp_v0": lambda: self.seal_mvp(state),
        }

        for step in self.activation_sequence:
            action = actions.get(step)
            if not action:
                continue
            action()
            state.checklist[step] = True

        self.memory_pack.add_memory(
            MemoryFragment(
                text=f"Activation complete for run {state.run_id}",
                tags=["activation", environment, state.seal_version],
                importance=2,
            )
        )
        return state