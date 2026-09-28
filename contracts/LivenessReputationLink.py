# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json

from genlayer import *
from dataclasses import dataclass

MIN_EPOCHS_OBSERVED = 3


@allow_storage
@dataclass
class LivenessChange:
    change_id: u256
    agent: str
    uptime_score: u256
    epochs_observed: u256
    change_type: str  # INCREASE, DECREASE


class LivenessReputationLink(gl.Contract):
    changes: TreeMap[u256, LivenessChange]
    applied: TreeMap[str, u256]
    reputation: TreeMap[str, u256]
    next_id: u256
    monitor_contract: str

    def __init__(self, monitor_address: str):
        self.next_id = u256(0)
        self.monitor_contract = monitor_address
        # No initialize method: reputation.get(agent, u256(50)) is a lazy default.

    @gl.public.write
    def apply_liveness(self, agent: str) -> u256:
        raw = gl.get_contract_at(
            Address(self.monitor_contract)
        ).view().get_service_data(agent)
        assert raw != "NOT_FOUND", "Service not found in monitor"

        try:
            data = json.loads(raw)
        except:
            raise gl.vm.UserError("Invalid data from monitor")

        observed = int(data.get("epochs_observed", 0))
        assert observed >= MIN_EPOCHS_OBSERVED, "Not enough epochs observed"

        applied_key = f"{agent}:{observed}"
        assert applied_key not in self.applied, "Already applied for this observation count"

        beats = int(data.get("total_beats", 0))
        uptime = (beats * 100) // observed

        current = self.reputation.get(agent, u256(50))
        new_score = u256(uptime)

        if new_score > current + u256(10):
            change_type = "INCREASE"
        elif new_score < current - u256(10):
            change_type = "DECREASE"
        else:
            raise gl.vm.UserError("Change too small to apply")

        self.reputation[agent] = new_score
        self.applied[applied_key] = u256(1)

        cid = self.next_id
        self.next_id += u256(1)
        self.changes[cid] = LivenessChange(
            change_id=cid,
            agent=agent,
            uptime_score=new_score,
            epochs_observed=u256(observed),
            change_type=change_type,
        )
        return cid

    @gl.public.view
    def get_reputation(self, agent: str) -> str:
        return f"REPUTATION:{int(self.reputation.get(agent, u256(50)))}"

    @gl.public.view
    def get_change_details(self, change_id: u256) -> str:
        if change_id not in self.changes:
            return "NOT_FOUND"
        c = self.changes[change_id]
        return json.dumps({
            "change_id": int(c.change_id),
            "agent": c.agent,
            "uptime_score": int(c.uptime_score),
            "epochs_observed": int(c.epochs_observed),
            "change_type": c.change_type,
        })

    @gl.public.view
    def list_changes(self) -> str:
        items = []
        for key in self.changes:
            c = self.changes[key]
            items.append(f"{int(c.change_id)}:{c.change_type}")
        return ",".join(items)
