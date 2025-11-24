# MAOS Activation Stack v1 — Master Codex

## Preface — Charter Standard Execution
The Activ8 AI Charter is supreme across every component in this repository. The codex enforces STOP–RESET–REALIGN, dual-agent resiliency, and immutability of custody records. Every run, commit, and artifact must be traceable to Genesis ID `GENESIS-ACTIV8-MAOS` and recorded in the Custodian Ledger.

---

## Layer 0 — Canonical Positioning
- Governs Activ8 AI, DMAOS, LMAOS, and authorized forks.
- Scope: activation, autonomy, governance, telemetry, custody, evidence, recovery.
- Traceability anchors: `configs/global_config.yaml` and `custody/ledger.db`.

## Layer 1 — Genesis Model
- Principle: governed autonomous multi-agent system with real-time telemetry and memory.
- Constraints: Charter supremacy, STOP–RESET–REALIGN override, dual-agent backup, no external relays, central timestamps (America/Chicago).

## Layer 2 — System Spine
Required directories (already provisioned):
`configs/`, `orchestration/`, `memory/`, `custody/`, `scripts/`, `agent_hub/`, `telemetry/`, `relay/`, `autonomy/`.

## Layer 3 — Core Pack v1 Codedrop
- MCP Relay Server (`orchestration/MCP/relay_server.py`).
- Memory Pack (`memory/sql_store`, `memory/vector_store`).
- Custodian Ledger + schema guard (`custody/ledger.py`).
- Telemetry Engine + relays (`telemetry/telemetry_engine.py`, `relay/*.py`).
- Autonomy Kernel (`autonomy/start_autonomy_loop.py`).
- Secrets Loader (`scripts/load_secrets_from_notion.py`).

## Layer 4 — Activation Sequence
`configs/global_config.yaml` encodes the canonical boot order:
1. verify_core_pack
2. install_dependencies
3. load_secrets
4. start_mcp
5. emit_heartbeat
6. activate_agents
7. start_autonomy_loop
8. seal_mvp_v0

`MCPRelayServer.run_activation` executes this sequence and updates the checklist.

## Layer 5 — Telemetry System
- Signals: heartbeat, load, drift, governance compliance, seal alignment, ledger health.
- Routes: Slack (`relay/slack_signalbot.py`), Notion (`relay/notion_relay.py`), Teamwork (`relay/teamwork_sink.py`).
- Drift guardrails: 0–10 green, 11–30 yellow, 31+ red → SRR trigger (`AutonomyLoop.stop_reset_realign`).

## Layer 6 — Governance System
- MCP requests flow through `MCPRelayServer` which enforces Charter guardrails.
- `AgentHub` logs every activation, ensures dual-agent state, and emits telemetry.
- Drift violations halt autonomy (`autonomy/start_autonomy_loop.py`).
- Seal changes invoke ledger checkpoints (`MCPRelayServer.seal_mvp`).
- RoleIDs defined in config; ledger enforces provenance.

## Layer 7 — Custodian Ledger
- Schema: `id, timestamp, event_type, actor_identity, payload, correlation_id, seal_version, environment`.
- Guarantees: append-only SQLite, auto-schema creation, genesis traceability.
- Access via `custody/ledger.py`.

## Layer 8 — Activation Log Protocol
`MCPRelayServer.run_activation` generates `run_id`, writes ledger entries per step, emits telemetry, and persists memory fragments for evidence linking.

## Layer 9 — Evidence System
| Pack | Contents | Location |
| --- | --- | --- |
| Slack Pack | heartbeat/load/drift | `.runtime/slack_signals.log` |
| Notion Pack | activation + seal entries | `.runtime/notion_signals.log` |
| Teamwork Pack | drift scores, ledger health | `.runtime/teamwork_signals.log` |

## Layer 10 — MVP Seal System
- Versions: MVP_v0 ignition, MVP_v1 integration, MVP_v2 orchestration, MVP_v3 KPI layer, MVP_v4 autonomy mesh.
- Seal conditions validated during activation checklist; recorded in `seals/MVP_v0_SEAL.md` and ledger.

## Layer 11 — Daily Autonomy Snapshot
Template: see Appendix D. Includes seal, drift, heartbeats, governance events, ledger health, system notes.

## Layer 12 — Governance Incident System
Triggers: drift > 30, governance violation, MCP anomaly, memory fault, seal misalignment.
Required actions: incident report filed (Appendix C), ledger cross-link, approvals, resolution log.

## Layer 13 — Client Intelligence Layer
Pull from Master Client Operational Matrix; tracked fields configured under `client_intelligence` in `global_config.yaml`.

## Layer 14 — Full System Checklist
Stored in config and rendered in `seals/MVP_v0_SEAL.md`. ACTIVE only when every box is checked true by MCP relay.

## Layer 15 — Master Summary
This codex contains architecture, governance, activation flows, telemetry, drift logic, evidence routes, seal policies, SOPs, runbooks, and incident templates—complete and reproducible.

## Layer 16 — The Four Pillars
**Composable • Fungible • Modular • Stackable**
Every artifact connects via explicit contracts, remains interchangeable under governance, adheres to single responsibility boundaries, and supports additive layering.

---

## Appendix A — Core Pack File Map
```
MAOS_Activation_Stack_v1/
├── configs/global_config.yaml
├── configs/config_loader.py
├── orchestration/MCP/relay_server.py
├── memory/sql_store/store.py
├── memory/vector_store/memory_pack.py
├── custody/ledger.db
├── custody/ledger.py
├── scripts/load_secrets_from_notion.py
├── agent_hub/activate.py
├── telemetry/telemetry_engine.py
├── relay/{base,slack_signalbot,notion_relay,teamwork_sink}.py
├── autonomy/start_autonomy_loop.py
├── seals/MVP_v0_SEAL.md
└── MAOS_BOOK.md
```

## Appendix B — Seal Template (MVP)
See `seals/MVP_v0_SEAL.md` for the canonical form. Future seals extend the same schema with additional readiness checks.

## Appendix C — Incident Report Template
```
Incident ID:
Run ID:
Triggered Layer:
Trigger Type (drift/governance/memory/seal):
Timestamps (America/Chicago):
Summary:
Impact Assessment:
STOP–RESET–REALIGN Invoked? (Y/N):
Corrective Actions:
Ledger Entry ID / Evidence Links:
Approvals (RoleID-Signature):
```

## Appendix D — Daily Autonomy Snapshot Template
```
Date (America/Chicago):
Seal Version:
Heartbeat Count:
Avg Drift Score:
Governance Events Logged:
Ledger Health:
Active Components:
Notes / Risks:
Evidence Links:
```

---

**Terminal Invocation:** Composable • Fungible • Modular • Stackable