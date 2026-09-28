# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json

from genlayer import *
from dataclasses import dataclass


@allow_storage
@dataclass
class FinalizedOutcome:
    poll_id: u256
    winner: str
    total_revealed: u256
    min_reveals_required: u256
    status: str  # FINALIZED


class CommitRevealResolver(gl.Contract):
    outcomes: TreeMap[u256, FinalizedOutcome]
    finalized_polls: TreeMap[u256, bool]
    vote_contract: str

    def __init__(self, vote_address: str):
        self.vote_contract = vote_address

    @gl.public.write
    def finalize_poll(self, poll_id: u256, min_reveals: u256) -> bool:
        assert poll_id not in self.finalized_polls, "Poll already finalized"
        assert min_reveals > u256(0), "min_reveals must be positive"

        raw = gl.get_contract_at(
            Address(self.vote_contract)
        ).view().get_poll_data(poll_id)

        assert raw != "NOT_FOUND", "Poll not found in vote contract"

        try:
            data = json.loads(raw)
        except:
            raise gl.vm.UserError("Invalid data from vote contract")

        status = data.get("status", "")
        assert status == "CLOSED", "Poll has not been closed yet"

        total_revealed = int(data.get("total_revealed", 0))
        assert total_revealed >= int(min_reveals), "Quorum not met"

        winner = data.get("winner", "")
        assert winner != "", "No winner recorded on the poll"

        self.outcomes[poll_id] = FinalizedOutcome(
            poll_id=poll_id,
            winner=winner,
            total_revealed=u256(total_revealed),
            min_reveals_required=min_reveals,
            status="FINALIZED",
        )
        self.finalized_polls[poll_id] = True

        return True

    @gl.public.view
    def get_outcome(self, poll_id: u256) -> str:
        if poll_id not in self.outcomes:
            return "NOT_FOUND"
        o = self.outcomes[poll_id]
        return json.dumps({
            "poll_id": int(o.poll_id),
            "winner": o.winner,
            "total_revealed": int(o.total_revealed),
            "min_reveals_required": int(o.min_reveals_required),
            "status": o.status,
        })

    @gl.public.view
    def is_finalized(self, poll_id: u256) -> str:
        return "FINALIZED" if poll_id in self.finalized_polls else "NOT_FINALIZED"

    @gl.public.view
    def list_outcomes(self) -> str:
        items = []
        for key in self.outcomes:
            o = self.outcomes[key]
            items.append(f"{int(o.poll_id)}:{o.winner}")
        return ",".join(items)
