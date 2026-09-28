# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json

from genlayer import *
from dataclasses import dataclass


@allow_storage
@dataclass
class ExecutionRecord:
    proposal_id: u256
    proposer: str
    outcome: str  # PASSED, REJECTED
    for_weight: u256
    against_weight: u256
    min_total_weight: u256


class ProposalExecutor(gl.Contract):
    executions: TreeMap[u256, ExecutionRecord]
    voting_contract: str

    def __init__(self, voting_address: str):
        self.voting_contract = voting_address

    @gl.public.write
    def execute_proposal(self, proposal_id: u256, min_total_weight: u256) -> str:
        assert proposal_id not in self.executions, "Proposal already executed"
        assert min_total_weight > u256(0), "min_total_weight must be positive"

        raw = gl.get_contract_at(
            Address(self.voting_contract)
        ).view().get_voting_data(proposal_id)
        assert raw != "NOT_FOUND", "Voting not found"

        try:
            data = json.loads(raw)
        except:
            raise gl.vm.UserError("Invalid data from voting contract")

        assert data.get("status", "") == "CLOSED", "Voting has not been closed yet"

        for_weight = int(data.get("for_weight", 0))
        against_weight = int(data.get("against_weight", 0))
        assert for_weight + against_weight >= int(min_total_weight), "Quorum not met"

        outcome = "PASSED" if for_weight > against_weight else "REJECTED"

        self.executions[proposal_id] = ExecutionRecord(
            proposal_id=proposal_id,
            proposer=data.get("proposer", ""),
            outcome=outcome,
            for_weight=u256(for_weight),
            against_weight=u256(against_weight),
            min_total_weight=min_total_weight,
        )
        return outcome

    @gl.public.view
    def get_execution_data(self, proposal_id: u256) -> str:
        if proposal_id not in self.executions:
            return "NOT_FOUND"
        e = self.executions[proposal_id]
        return json.dumps({
            "proposal_id": int(e.proposal_id),
            "proposer": e.proposer,
            "outcome": e.outcome,
            "for_weight": int(e.for_weight),
            "against_weight": int(e.against_weight),
            "min_total_weight": int(e.min_total_weight),
        })

    @gl.public.view
    def list_executions(self) -> str:
        items = []
        for key in self.executions:
            e = self.executions[key]
            items.append(f"{int(e.proposal_id)}:{e.outcome}")
        return ",".join(items)
