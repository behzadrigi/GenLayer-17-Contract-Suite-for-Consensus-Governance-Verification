# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import re

from genlayer import *
from dataclasses import dataclass

MAX_STAGES = 3
SUPPORT_LABELS = ("SUPPORTED", "UNSUPPORTED")
CHALLENGE_LABELS = ("SUPPORTED", "OVERTURNED")


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


def first_label(text: str, labels: tuple, default: str) -> str:
    for word in re.findall(r"[A-Z_]+", str(text).upper()):
        if word in labels:
            return word
    return default


def fetch_text(url: str) -> str:
    try:
        return gl.nondet.web.render(url)
    except:
        return ""


def judge_support(statement: str, evidence_url: str) -> str:
    content = fetch_text(evidence_url)
    if content.strip() == "":
        return "UNSUPPORTED"

    prompt = f"""
    Statement: {statement}

    Evidence ({evidence_url}):
    {content[:2500]}

    Does this evidence SUPPORT the statement?
    Respond with ONLY one word: SUPPORTED or UNSUPPORTED.
    """
    response = gl.nondet.exec_prompt(prompt)
    return first_label(response, SUPPORT_LABELS, "UNSUPPORTED")


def judge_challenge(statement: str, evidence_url: str, counter_url: str) -> str:
    counter = fetch_text(counter_url)
    if counter.strip() == "":
        # A challenge with no retrievable counter-evidence cannot overturn anything.
        return "SUPPORTED"
    original = fetch_text(evidence_url)

    prompt = f"""
    Statement: {statement}

    Original evidence ({evidence_url}):
    {original[:1800]}

    Counter-evidence ({counter_url}):
    {counter[:1800]}

    Weighing both, is the statement still SUPPORTED, or has it been OVERTURNED
    by the counter-evidence?
    Respond with ONLY one word: SUPPORTED or OVERTURNED.
    """
    response = gl.nondet.exec_prompt(prompt)
    return first_label(response, CHALLENGE_LABELS, "SUPPORTED")


@allow_storage
@dataclass
class Assertion:
    assertion_id: u256
    asserter: str
    statement: str
    evidence_url: str
    challenger: str
    counter_url: str
    stage: u256
    status: str  # PENDING, ACCEPTED, REJECTED, CHALLENGED, FINALIZED_ACCEPTED, FINALIZED_OVERTURNED


class ChallengeableAssertion(gl.Contract):
    assertions: TreeMap[u256, Assertion]
    next_id: u256

    def __init__(self):
        self.next_id = u256(0)

    @gl.public.write
    def assert_claim(self, statement: str, evidence_url: str) -> u256:
        assert statement.strip() != "", "Statement cannot be empty"
        cleaned = clean_url(evidence_url)
        assert cleaned is not None, f"Invalid evidence URL: {evidence_url}"
        assert is_valid_url(cleaned), f"Invalid evidence URL: {cleaned}"

        aid = self.next_id
        self.next_id += u256(1)
        self.assertions[aid] = Assertion(
            assertion_id=aid,
            asserter=str(gl.message.sender_address),
            statement=statement,
            evidence_url=cleaned,
            challenger="",
            counter_url="",
            stage=u256(0),
            status="PENDING",
        )
        return aid

    @gl.public.write
    def evaluate(self, assertion_id: u256) -> bool:
        assert assertion_id in self.assertions, "Assertion not found"
        a = self.assertions[assertion_id]
        assert a.status == "PENDING", "Assertion already evaluated"

        statement = a.statement
        evidence_url = a.evidence_url

        # Stage 1 — Equivalence Principle: STRICT EQUALITY on a two-way label.
        def leader_fn():
            return {"label": judge_support(statement, evidence_url)}

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            leader_label = leader_result.calldata.get("label")
            if leader_label not in SUPPORT_LABELS:
                return False
            return judge_support(statement, evidence_url) == leader_label

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        a.stage = u256(1)
        a.status = "ACCEPTED" if result["label"] == "SUPPORTED" else "REJECTED"
        self.assertions[assertion_id] = a
        return True

    @gl.public.write
    def challenge(self, assertion_id: u256, counter_url: str):
        assert assertion_id in self.assertions, "Assertion not found"
        a = self.assertions[assertion_id]
        assert a.status == "ACCEPTED", "Only an accepted assertion can be challenged"
        assert a.stage < u256(MAX_STAGES), "Assertion can no longer be challenged"

        challenger = str(gl.message.sender_address)
        assert challenger != a.asserter, "Asserter cannot challenge their own assertion"

        cleaned = clean_url(counter_url)
        assert cleaned is not None, f"Invalid counter URL: {counter_url}"
        assert is_valid_url(cleaned), f"Invalid counter URL: {cleaned}"
        assert cleaned != a.evidence_url, "Counter-evidence must differ from the original evidence"
        assert cleaned != a.counter_url, "Counter-evidence must differ from the previous counter-evidence"

        a.challenger = challenger
        a.counter_url = cleaned
        a.status = "CHALLENGED"
        self.assertions[assertion_id] = a

    @gl.public.write
    def resolve_challenge(self, assertion_id: u256) -> bool:
        assert assertion_id in self.assertions, "Assertion not found"
        a = self.assertions[assertion_id]
        assert a.status == "CHALLENGED", "Assertion is not under challenge"

        statement = a.statement
        evidence_url = a.evidence_url
        counter_url = a.counter_url

        # Escalation stage — Equivalence Principle: STRICT EQUALITY, now weighing
        # the original evidence against the challenger's counter-evidence.
        def leader_fn():
            return {"label": judge_challenge(statement, evidence_url, counter_url)}

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            leader_label = leader_result.calldata.get("label")
            if leader_label not in CHALLENGE_LABELS:
                return False
            return judge_challenge(statement, evidence_url, counter_url) == leader_label

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        new_stage = int(a.stage) + 1
        a.stage = u256(new_stage)
        if result["label"] == "OVERTURNED":
            a.status = "FINALIZED_OVERTURNED"
        elif new_stage >= MAX_STAGES:
            a.status = "FINALIZED_ACCEPTED"
        else:
            a.status = "ACCEPTED"
        self.assertions[assertion_id] = a
        return True

    @gl.public.view
    def get_assertion_data(self, assertion_id: u256) -> str:
        if assertion_id not in self.assertions:
            return "NOT_FOUND"
        a = self.assertions[assertion_id]
        return json.dumps({
            "assertion_id": int(a.assertion_id),
            "asserter": a.asserter,
            "statement": a.statement,
            "evidence_url": a.evidence_url,
            "challenger": a.challenger,
            "counter_url": a.counter_url,
            "stage": int(a.stage),
            "status": a.status,
        })

    @gl.public.view
    def list_assertions(self) -> str:
        items = []
        for key in self.assertions:
            a = self.assertions[key]
            items.append(f"{int(a.assertion_id)}:{a.status}")
        return ",".join(items)
