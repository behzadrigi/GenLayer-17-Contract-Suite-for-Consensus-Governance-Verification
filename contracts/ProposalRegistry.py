# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json

from genlayer import *
from dataclasses import dataclass


@allow_storage
@dataclass
class Proposal:
    proposal_id: u256
    proposer: str
    title: str
    description: str


class ProposalRegistry(gl.Contract):
    proposals: TreeMap[u256, Proposal]
    next_id: u256

    def __init__(self):
        self.next_id = u256(0)

    @gl.public.write
    def create_proposal(self, title: str, description: str) -> u256:
        assert title.strip() != "", "Title cannot be empty"
        assert description.strip() != "", "Description cannot be empty"

        pid = self.next_id
        self.next_id += u256(1)
        self.proposals[pid] = Proposal(
            proposal_id=pid,
            proposer=str(gl.message.sender_address),
            title=title,
            description=description,
        )
        return pid

    @gl.public.view
    def get_proposal_data(self, proposal_id: u256) -> str:
        if proposal_id not in self.proposals:
            return "NOT_FOUND"
        p = self.proposals[proposal_id]
        return json.dumps({
            "proposal_id": int(p.proposal_id),
            "proposer": p.proposer,
            "title": p.title,
            "description": p.description,
        })

    @gl.public.view
    def list_proposals(self) -> str:
        items = []
        for key in self.proposals:
            p = self.proposals[key]
            items.append(f"{int(p.proposal_id)}:{p.title}")
        return ",".join(items)
