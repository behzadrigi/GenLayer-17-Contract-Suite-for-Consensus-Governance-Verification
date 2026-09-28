# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import re

from genlayer import *
from dataclasses import dataclass

ANSWERS = ("YES", "NO", "UNCLEAR")


def first_label(text: str, labels: tuple, default: str) -> str:
    for word in re.findall(r"[A-Z_]+", str(text).upper()):
        if word in labels:
            return word
    return default


def resolve_question(question: str, source_url: str) -> dict:
    try:
        content = gl.nondet.web.render(source_url)
    except:
        content = ""
    if content.strip() == "":
        return {"source_fetched": False, "answer": "UNCLEAR"}

    prompt = f"""
    Question: {question}

    Source content ({source_url}):
    {content[:2500]}

    Based ONLY on this source, is the answer to the question YES, NO, or UNCLEAR?
    Respond with ONLY one word: YES, NO, or UNCLEAR.
    """
    response = gl.nondet.exec_prompt(prompt)
    return {"source_fetched": True, "answer": first_label(response, ANSWERS, "UNCLEAR")}


@allow_storage
@dataclass
class Resolution:
    market_id: u256
    outcome: str  # YES, NO, UNRESOLVED
    answer: str
    source_fetched: bool
    status: str  # RESOLVED


class MarketOracleSettlement(gl.Contract):
    resolutions: TreeMap[u256, Resolution]
    market_contract: str

    def __init__(self, market_address: str):
        self.market_contract = market_address

    @gl.public.write
    def resolve_market(self, market_id: u256) -> bool:
        assert market_id not in self.resolutions, "Market already resolved"

        raw = gl.get_contract_at(
            Address(self.market_contract)
        ).view().get_market_data(market_id)
        assert raw != "NOT_FOUND", "Market not found"

        try:
            data = json.loads(raw)
        except:
            raise gl.vm.UserError("Invalid data from market")

        assert data.get("status", "") == "CLOSED", "Market must be closed before resolution"

        question = data.get("question", "")
        source_url = data.get("source_url", "")

        # Equivalence Principle: COMPARATIVE, two-field, web-grounded. The
        # contract fetches the market's own source page itself.
        def leader_fn():
            return resolve_question(question, source_url)

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            leader_data = leader_result.calldata
            if not isinstance(leader_data.get("source_fetched"), bool):
                return False
            if leader_data.get("answer") not in ANSWERS:
                return False
            mine = resolve_question(question, source_url)
            return (
                mine["source_fetched"] == leader_data["source_fetched"]
                and mine["answer"] == leader_data["answer"]
            )

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        if result["source_fetched"] and result["answer"] in ("YES", "NO"):
            outcome = result["answer"]
        else:
            outcome = "UNRESOLVED"

        self.resolutions[market_id] = Resolution(
            market_id=market_id,
            outcome=outcome,
            answer=result["answer"],
            source_fetched=result["source_fetched"],
            status="RESOLVED",
        )
        return True

    @gl.public.view
    def get_resolution_data(self, market_id: u256) -> str:
        if market_id not in self.resolutions:
            return "NOT_FOUND"
        r = self.resolutions[market_id]
        return json.dumps({
            "market_id": int(r.market_id),
            "outcome": r.outcome,
            "answer": r.answer,
            "source_fetched": r.source_fetched,
            "status": r.status,
        })

    @gl.public.view
    def list_resolutions(self) -> str:
        items = []
        for key in self.resolutions:
            r = self.resolutions[key]
            items.append(f"{int(r.market_id)}:{r.outcome}")
        return ",".join(items)
