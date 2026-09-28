# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import hashlib

from genlayer import *
from dataclasses import dataclass


def compute_commitment(choice: str, salt: str) -> str:
    return hashlib.sha256(f"{choice}:{salt}".encode()).hexdigest()


@allow_storage
@dataclass
class Poll:
    poll_id: u256
    creator: str
    question: str
    options: str  # comma-separated
    status: str  # COMMIT, REVEAL, CLOSED
    total_revealed: u256
    winner: str


@allow_storage
@dataclass
class Commitment:
    voter: str
    commitment_hash: str
    revealed: bool
    revealed_choice: str


class CommitRevealVote(gl.Contract):
    polls: TreeMap[u256, Poll]
    # key: "{poll_id}:{voter_address}"
    commitments: TreeMap[str, Commitment]
    # key: "{poll_id}:{option}"
    tallies: TreeMap[str, u256]
    next_id: u256

    def __init__(self):
        self.next_id = u256(0)

    @gl.public.write
    def create_poll(self, question: str, options: str) -> u256:
        assert question.strip() != "", "Question cannot be empty"
        option_list = [o.strip() for o in options.split(',') if o.strip()]
        assert len(option_list) >= 2, "At least 2 options required"
        assert len(set(option_list)) == len(option_list), "Duplicate options"

        pid = self.next_id
        self.next_id += u256(1)

        self.polls[pid] = Poll(
            poll_id=pid,
            creator=str(gl.message.sender_address),
            question=question,
            options=",".join(option_list),
            status="COMMIT",
            total_revealed=u256(0),
            winner="",
        )

        return pid

    @gl.public.write
    def commit_vote(self, poll_id: u256, commitment_hash: str):
        assert poll_id in self.polls, "Poll not found"
        poll = self.polls[poll_id]
        assert poll.status == "COMMIT", "Poll is not in commit phase"
        assert commitment_hash.strip() != "", "Commitment cannot be empty"

        voter = str(gl.message.sender_address)
        key = f"{int(poll_id)}:{voter}"
        assert key not in self.commitments, "Already committed to this poll"

        self.commitments[key] = Commitment(
            voter=voter,
            commitment_hash=commitment_hash.strip().lower(),
            revealed=False,
            revealed_choice="",
        )

    @gl.public.write
    def advance_to_reveal(self, poll_id: u256):
        assert poll_id in self.polls, "Poll not found"
        poll = self.polls[poll_id]
        assert str(gl.message.sender_address) == poll.creator, "Only creator can advance the poll"
        assert poll.status == "COMMIT", "Poll must be in commit phase"

        poll.status = "REVEAL"
        self.polls[poll_id] = poll

    @gl.public.write
    def reveal_vote(self, poll_id: u256, choice: str, salt: str):
        assert poll_id in self.polls, "Poll not found"
        poll = self.polls[poll_id]
        assert poll.status == "REVEAL", "Poll is not in reveal phase"

        option_list = [o.strip() for o in poll.options.split(',')]
        assert choice.strip() in option_list, "Choice is not a valid option for this poll"

        voter = str(gl.message.sender_address)
        key = f"{int(poll_id)}:{voter}"
        assert key in self.commitments, "No commitment found for this voter"

        commitment = self.commitments[key]
        assert not commitment.revealed, "Already revealed"

        expected_hash = compute_commitment(choice.strip(), salt)
        assert expected_hash == commitment.commitment_hash, "Revealed choice does not match commitment"

        commitment.revealed = True
        commitment.revealed_choice = choice.strip()
        self.commitments[key] = commitment

        tally_key = f"{int(poll_id)}:{choice.strip()}"
        current = self.tallies.get(tally_key, u256(0))
        self.tallies[tally_key] = current + u256(1)

        poll.total_revealed += u256(1)
        self.polls[poll_id] = poll

    @gl.public.write
    def close_poll(self, poll_id: u256) -> str:
        assert poll_id in self.polls, "Poll not found"
        poll = self.polls[poll_id]
        assert str(gl.message.sender_address) == poll.creator, "Only creator can close the poll"
        assert poll.status == "REVEAL", "Poll must be in reveal phase to close"
        assert poll.total_revealed > u256(0), "At least one reveal is required to close"

        option_list = [o.strip() for o in poll.options.split(',')]
        best_option = ""
        best_count = -1
        for opt in option_list:
            tally_key = f"{int(poll_id)}:{opt}"
            count = int(self.tallies.get(tally_key, u256(0)))
            if count > best_count:
                best_count = count
                best_option = opt

        poll.status = "CLOSED"
        poll.winner = best_option
        self.polls[poll_id] = poll

        return best_option

    @gl.public.view
    def get_poll_status(self, poll_id: u256) -> str:
        if poll_id not in self.polls:
            return "NOT_FOUND"
        return self.polls[poll_id].status

    @gl.public.view
    def get_poll_data(self, poll_id: u256) -> str:
        if poll_id not in self.polls:
            return "NOT_FOUND"
        p = self.polls[poll_id]
        return json.dumps({
            "poll_id": int(p.poll_id),
            "creator": p.creator,
            "question": p.question,
            "options": p.options,
            "status": p.status,
            "total_revealed": int(p.total_revealed),
            "winner": p.winner,
        })

    @gl.public.view
    def get_tally(self, poll_id: u256, option: str) -> str:
        tally_key = f"{int(poll_id)}:{option.strip()}"
        return str(int(self.tallies.get(tally_key, u256(0))))

    @gl.public.view
    def get_commitment_status(self, poll_id: u256, voter: str) -> str:
        key = f"{int(poll_id)}:{voter}"
        if key not in self.commitments:
            return "NOT_FOUND"
        c = self.commitments[key]
        return "REVEALED" if c.revealed else "COMMITTED"

    @gl.public.view
    def list_polls(self) -> str:
        items = []
        for key in self.polls:
            p = self.polls[key]
            items.append(f"{int(p.poll_id)}:{p.status}")
        return ",".join(items)
