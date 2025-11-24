"""
Agent activation hub with Charter guardrails.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from configs.config_loader import load_config
from custody.ledger import CustodianLedger, LedgerEvent
from telemetry.telemetry_engine import TelemetryEngine, TelemetryRecord


@dataclass
class AgentProfile:
    agent_id: str
    role: str
    tier: str
    status: str = field(default="idle")


class AgentHub:
    def __init__(self, ledger: CustodianLedger, telemetry: TelemetryEngine) -> None:
        config = load_config()
        self.agents: Dict[str, AgentProfile] = {
            agent_cfg["id"]: AgentProfile(
                agent_cfg["id"], agent_cfg["role"], agent_cfg["tier"]
            )
            for agent_cfg in config.get("agents", [])
        }
        self.dual_backup_required = config.get("autonomy", {}).get(
            "dual_agent_backup", True
        )
        self.ledger = ledger
        self.telemetry = telemetry

    def _ensure_dual_agent_state(self) -> None:
        if not self.dual_backup_required:
            return
        primary_online = any(
            profile.tier == "primary" and profile.status == "online"
            for profile in self.agents.values()
        )
        backup_online = any(
            profile.tier != "primary" and profile.status == "online"
            for profile in self.agents.values()
        )
        if not (primary_online and backup_online):
            raise RuntimeError(
                "Dual-Agent Backup requirement violated: ensure primary and backup online."
            )

    def activate_agents(self, run_id: str, environment: str) -> List[str]:
        activated: List[str] = []
        for profile in self.agents.values():
            profile.status = "online"
            activated.append(profile.agent_id)
            self.ledger.write_event(
                LedgerEvent(
                    event_type="agent_activation",
                    actor_identity=profile.agent_id,
                    payload={"role": profile.role, "tier": profile.tier},
                    correlation_id=run_id,
                    seal_version="MVP_v0",
                    environment=environment,
                )
            )
        self._ensure_dual_agent_state()
        self.telemetry.emit(
            TelemetryRecord(
                signal_type="agent_hub",
                payload={"activated": ",".join(activated), "run_id": run_id},
            )
        )
        return activated

    def status_report(self) -> Dict[str, str]:
        return {agent_id: profile.status for agent_id, profile in self.agents.items()}