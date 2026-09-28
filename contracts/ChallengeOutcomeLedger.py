# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json

from genlayer import *
from dataclasses import dataclass

FINAL_STATUSES = ("FINALIZED_ACCEPTED", "FINALIZED_OVERTURNED", "REJECTED")


@allow_storage
@dataclass
class OutcomeRecord:
    assertion_id: u256
    asserter: str
    final_status: str
    stages: u256
    upheld: bool


class ChallengeOutcomeLedger(gl.Contract):
    outcomes: TreeMap[u256, OutcomeRecord]
    upheld_counts: TreeMap[str, u256]
    lost_counts: TreeMap[str, u256]
    assertion_contract: str

    def __init__(self, assertion_address: str):
        self.assertion_contract = assertion_address

    @gl.public.write
    def record_outcome(self, assertion_id: u256) -> bool:
        assert assertion_id not in self.outcomes, "Outcome already recorded"

        raw = gl.get_contract_at(
            Address(self.assertion_contract)
        ).view().get_assertion_data(assertion_id)
        assert raw != "NOT_FOUND", "Assertion not found"

        try:
            data = json.loads(raw)
        except:
            raise gl.vm.UserError("Invalid data from assertion contract")

        final_status = data.get("status", "")
        assert final_status in FINAL_STATUSES, "Assertion has not reached a final status"

        asserter = data.get("asserter", "")
        assert asserter != "", "Asserter not found in assertion record"

        upheld = final_status == "FINALIZED_ACCEPTED"
        self.outcomes[assertion_id] = OutcomeRecord(
            assertion_id=assertion_id,
            asserter=asserter,
            final_status=final_status,
            stages=u256(int(data.get("stage", 0))),
            upheld=upheld,
        )
        if upheld:
            self.upheld_counts[asserter] = self.upheld_counts.get(asserter, u256(0)) + u256(1)
        else:
            self.lost_counts[asserter] = self.lost_counts.get(asserter, u256(0)) + u256(1)
        return True

    @gl.public.view
    def get_outcome_data(self, assertion_id: u256) -> str:
        if assertion_id not in self.outcomes:
            return "NOT_FOUND"
        o = self.outcomes[assertion_id]
        return json.dumps({
            "assertion_id": int(o.assertion_id),
            "asserter": o.asserter,
            "final_status": o.final_status,
            "stages": int(o.stages),
            "upheld": o.upheld,
        })

    @gl.public.view
    def get_agent_record(self, agent: str) -> str:
        return json.dumps({
            "agent": agent,
            "upheld": int(self.upheld_counts.get(agent, u256(0))),
            "lost": int(self.lost_counts.get(agent, u256(0))),
        })

    @gl.public.view
    def list_outcomes(self) -> str:
        items = []
        for key in self.outcomes:
            o = self.outcomes[key]
            items.append(f"{int(o.assertion_id)}:{o.final_status}")
        return ",".join(items)
