# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import re

from genlayer import *
from dataclasses import dataclass


def clean_url(url: str):
    if not url:
        return None
    cleaned = url.strip().rstrip('/')
    if cleaned.startswith('http://'):
        cleaned = cleaned.replace('http://', 'https://', 1)
    cleaned = cleaned.replace(' ', '')
    if '?' in cleaned:
        cleaned = cleaned.split('?')[0]
    return cleaned if cleaned else None


def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r'^(https?://)'
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
        r'(/[\w\-./?%&=]*)?$'
    )
    return bool(pattern.match(url.strip()))


@allow_storage
@dataclass
class ProofRecord:
    proof_id: u256
    author: str
    statement: str
    proof_url: str
    status: str  # SUBMITTED


class ProofRegistry(gl.Contract):
    proofs: TreeMap[u256, ProofRecord]
    next_id: u256

    def __init__(self):
        self.next_id = u256(0)

    @gl.public.write
    def submit_proof(self, statement: str, proof_url: str) -> u256:
        assert statement.strip() != "", "Statement cannot be empty"
        cleaned = clean_url(proof_url)
        assert cleaned is not None, f"Invalid proof URL: {proof_url}"
        assert is_valid_url(cleaned), f"Invalid proof URL: {cleaned}"

        pid = self.next_id
        self.next_id += u256(1)
        self.proofs[pid] = ProofRecord(
            proof_id=pid,
            author=str(gl.message.sender_address),
            statement=statement,
            proof_url=cleaned,
            status="SUBMITTED",
        )
        return pid

    @gl.public.view
    def get_proof_data(self, proof_id: u256) -> str:
        if proof_id not in self.proofs:
            return "NOT_FOUND"
        p = self.proofs[proof_id]
        return json.dumps({
            "proof_id": int(p.proof_id),
            "author": p.author,
            "statement": p.statement,
            "proof_url": p.proof_url,
            "status": p.status,
        })

    @gl.public.view
    def list_proofs(self) -> str:
        items = []
        for key in self.proofs:
            p = self.proofs[key]
            items.append(f"{int(p.proof_id)}:{p.status}")
        return ",".join(items)

    @gl.public.view
    def get_author_proofs(self, author: str) -> str:
        items = []
        for key in self.proofs:
            p = self.proofs[key]
            if p.author == author:
                items.append(str(int(p.proof_id)))
        return ",".join(items)
