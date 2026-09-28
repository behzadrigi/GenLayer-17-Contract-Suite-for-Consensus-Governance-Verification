# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import re

from genlayer import *
from dataclasses import dataclass

VERDICTS = ("VALID", "INVALID", "INCOMPLETE")


def first_label(text: str, labels: tuple, default: str) -> str:
    for word in re.findall(r"[A-Z_]+", str(text).upper()):
        if word in labels:
            return word
    return default


def check_proof_text(statement: str, proof_url: str) -> str:
    try:
        content = gl.nondet.web.render(proof_url)
    except:
        return "INCOMPLETE"
    if content.strip() == "":
        return "INCOMPLETE"

    prompt = f"""
    Statement to be proven: {statement}

    Written argument ({proof_url}):
    {content[:3000]}

    Does this written argument correctly and completely prove the statement?
    Respond with ONLY one word:
    VALID (the argument is correct and complete),
    INVALID (the argument contains an error or proves something else),
    INCOMPLETE (steps are missing, or it is not a proof of this statement).
    """
    response = gl.nondet.exec_prompt(prompt)
    return first_label(response, VERDICTS, "INCOMPLETE")


@allow_storage
@dataclass
class CheckRecord:
    proof_id: u256
    author: str
    verdict: str
    status: str  # CHECKED


class StructuredProofChecker(gl.Contract):
    checks: TreeMap[u256, CheckRecord]
    registry_contract: str

    def __init__(self, registry_address: str):
        self.registry_contract = registry_address

    @gl.public.write
    def check_proof(self, proof_id: u256) -> bool:
        assert proof_id not in self.checks, "Already checked"

        raw = gl.get_contract_at(
            Address(self.registry_contract)
        ).view().get_proof_data(proof_id)
        assert raw != "NOT_FOUND", "Proof not found in registry"

        try:
            data = json.loads(raw)
        except:
            raise gl.vm.UserError("Invalid data from registry")

        author = data.get("author", "")
        statement = data.get("statement", "")
        proof_url = data.get("proof_url", "")
        assert author != "", "Author not found in proof record"

        # Equivalence Principle: STRICT EQUALITY on a three-way verdict.
        def leader_fn():
            return {"verdict": check_proof_text(statement, proof_url)}

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            leader_verdict = leader_result.calldata.get("verdict")
            if leader_verdict not in VERDICTS:
                return False
            return check_proof_text(statement, proof_url) == leader_verdict

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        self.checks[proof_id] = CheckRecord(
            proof_id=proof_id,
            author=author,
            verdict=result["verdict"],
            status="CHECKED",
        )
        return True

    @gl.public.view
    def get_check_data(self, proof_id: u256) -> str:
        if proof_id not in self.checks:
            return "NOT_FOUND"
        c = self.checks[proof_id]
        return json.dumps({
            "proof_id": int(c.proof_id),
            "author": c.author,
            "verdict": c.verdict,
            "status": c.status,
        })

    @gl.public.view
    def list_checks(self) -> str:
        items = []
        for key in self.checks:
            c = self.checks[key]
            items.append(f"{int(c.proof_id)}:{c.verdict}")
        return ",".join(items)
