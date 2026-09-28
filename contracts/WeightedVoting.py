# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json

from genlayer import *
from dataclasses import dataclass

BASELINE_REPUTATION = 50


def parse_reputation(raw: str) -> int:
    try:
        return int(str(raw).split(":")[1])
    except:
        return 0


@allow_storage
@dataclass
class VotingState:
    proposal_id: u256
    proposer: str
    status: str  # OPEN, CLOSED
    for_weight: u256
    against_weight: u256
    voter_count: u256


class WeightedVoting(gl.Contract):
    states: TreeMap[u256, VotingState]
    votes: TreeMap[str, u256]
    registry_contract: str
    reputation_contract: str

    def __init__(self, registry_address: str, reputation_address: str):
        self.registry_contract = registry_address
        self.reputation_contract = reputation_address

    @gl.public.write
    def open_voting(self, proposal_id: u256):
        assert proposal_id not in self.states, "Voting already opened"

        raw = gl.get_contract_at(
            Address(self.registry_contract)
        ).view().get_proposal_data(proposal_id)
        assert raw != "NOT_FOUND", "Proposal not found in registry"

        try:
            data = json.loads(raw)
        except:
            raise gl.vm.UserError("Invalid data from registry")

        proposer = data.get("proposer", "")
        assert str(gl.message.sender_address) == proposer, "Only the proposer can open voting"

        self.states[proposal_id] = VotingState(
            proposal_id=proposal_id,
            proposer=proposer,
            status="OPEN",
            for_weight=u256(0),
            against_weight=u256(0),
            voter_count=u256(0),
        )

    @gl.public.write
    def cast_vote(self, proposal_id: u256, support: str):
        assert proposal_id in self.states, "Voting not opened for this proposal"
        state = self.states[proposal_id]
        assert state.status == "OPEN", "Voting is not open"

        choice = support.strip().upper()
        assert choice in ("FOR", "AGAINST"), "Support must be FOR or AGAINST"

        voter = str(gl.message.sender_address)
        vote_key = f"{int(proposal_id)}:{voter}"
        assert vote_key not in self.votes, "Already voted"

        # Voting power is the voter's reputation ABOVE the baseline, read from
        # the reputation contract itself. A fresh address sits at the baseline
        # and has zero power, so spinning up new addresses buys nothing.
        rep_raw = gl.get_contract_at(
            Address(self.reputation_contract)
        ).view().get_reputation(voter)
        weight = max(0, parse_reputation(rep_raw) - BASELINE_REPUTATION)
        assert weight > 0, "No voting power"

        if choice == "FOR":
            state.for_weight = state.for_weight + u256(weight)
        else:
            state.against_weight = state.against_weight + u256(weight)
        state.voter_count = state.voter_count + u256(1)

        self.states[proposal_id] = state
        self.votes[vote_key] = u256(1)

    @gl.public.write
    def close_voting(self, proposal_id: u256):
        assert proposal_id in self.states, "Voting not opened for this proposal"
        state = self.states[proposal_id]
        assert str(gl.message.sender_address) == state.proposer, "Only the proposer can close voting"
        assert state.status == "OPEN", "Voting is not open"
        assert state.voter_count > u256(0), "At least one vote is required to close"

        state.status = "CLOSED"
        self.states[proposal_id] = state

    @gl.public.view
    def get_voting_data(self, proposal_id: u256) -> str:
        if proposal_id not in self.states:
            return "NOT_FOUND"
        s = self.states[proposal_id]
        return json.dumps({
            "proposal_id": int(s.proposal_id),
            "proposer": s.proposer,
            "status": s.status,
            "for_weight": int(s.for_weight),
            "against_weight": int(s.against_weight),
            "voter_count": int(s.voter_count),
        })

    @gl.public.view
    def has_voted(self, proposal_id: u256, voter: str) -> str:
        return "VOTED" if f"{int(proposal_id)}:{voter}" in self.votes else "NOT_VOTED"

    @gl.public.view
    def list_voting(self) -> str:
        items = []
        for key in self.states:
            s = self.states[key]
            items.append(f"{int(s.proposal_id)}:{s.status}")
        return ",".join(items)
