"""
Autonomy Kernel starter with STOP-RESET-REALIGN enforcement.
"""

from __future__ import annotations

import random
import time

from custody.ledger import CustodianLedger, LedgerEvent
from memory.vector_store.memory_pack import MemoryFragment, MemoryPack
from telemetry.telemetry_engine import TelemetryEngine


class AutonomyLoop:
    def __init__(
        self,
        ledger: CustodianLedger,
        telemetry: TelemetryEngine,
        memory_pack: MemoryPack,
        loop_interval: int = 5,
    ) -> None:
        self.ledger = ledger
        self.telemetry = telemetry
        self.memory_pack = memory_pack
        self.loop_interval = loop_interval
        self.reset_requested = False

    def stop_reset_realign(self, run_id: str, reason: str) -> None:
        self.reset_requested = True
        self.ledger.write_event(
            LedgerEvent(
                event_type="stop_reset_realign",
                actor_identity="autonomy_kernel",
                payload={"reason": reason},
                correlation_id=run_id,
                seal_version="MVP_v0",
                environment="kernel",
            )
        )
        self.telemetry.emit_drift(100, run_id)

    def run_once(self, run_id: str, environment: str) -> None:
        drift_score = random.randint(0, 25)
        drift_level = self.telemetry.emit_drift(drift_score, run_id)
        if drift_level == "red":
            self.stop_reset_realign(run_id, "drift red threshold reached")
            return

        self.memory_pack.add_memory(
            MemoryFragment(
                text=f"Autonomy loop executed for {run_id} in {environment}",
                tags=["autonomy", environment, drift_level],
                importance=1,
            )
        )

        self.ledger.write_event(
            LedgerEvent(
                event_type="autonomy_cycle",
                actor_identity="autonomy_kernel",
                payload={"drift_score": drift_score, "drift_level": drift_level},
                correlation_id=run_id,
                seal_version="MVP_v0",
                environment=environment,
            )
        )

        time.sleep(self.loop_interval)