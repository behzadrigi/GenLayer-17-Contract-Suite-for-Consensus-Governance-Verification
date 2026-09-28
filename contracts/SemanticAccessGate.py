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


def ask_yes_no(content: str, question: str) -> bool:
    prompt = f"""
    Page content (truncated):
    {content[:2500]}

    Question: {question}
    Respond with ONLY: YES or NO
    """
    response = gl.nondet.exec_prompt(prompt)
    for word in re.findall(r"[A-Z]+", str(response).upper()):
        if word in ("YES", "NO"):
            return word == "YES"
    return False


def assess_access(evidence_url: str, policy: str) -> dict:
    try:
        content = gl.nondet.web.render(evidence_url)
    except:
        content = ""
    if content.strip() == "":
        return {"meets_policy": False, "evidence_relevant": False}

    return {
        "meets_policy": ask_yes_no(
            content,
            f"Does this page demonstrate that its subject satisfies this access policy: {policy}",
        ),
        "evidence_relevant": ask_yes_no(
            content,
            "Is this page substantive, specific, and relevant as evidence of qualifications (not empty, generic, or unrelated)?",
        ),
    }


@allow_storage
@dataclass
class Resource:
    resource_id: u256
    owner: str
    name: str
    policy: str


@allow_storage
@dataclass
class AccessRequest:
    request_id: u256
    resource_id: u256
    requester: str
    evidence_url: str
    meets_policy: bool
    evidence_relevant: bool
    decision: str  # PENDING, GRANTED, DENIED


class SemanticAccessGate(gl.Contract):
    resources: TreeMap[u256, Resource]
    requests: TreeMap[u256, AccessRequest]
    grants: TreeMap[str, u256]
    next_resource_id: u256
    next_request_id: u256

    def __init__(self):
        self.next_resource_id = u256(0)
        self.next_request_id = u256(0)

    @gl.public.write
    def register_resource(self, name: str, policy: str) -> u256:
        assert name.strip() != "", "Name cannot be empty"
        assert policy.strip() != "", "Policy cannot be empty"

        rid = self.next_resource_id
        self.next_resource_id += u256(1)
        self.resources[rid] = Resource(
            resource_id=rid,
            owner=str(gl.message.sender_address),
            name=name,
            policy=policy,
        )
        return rid

    @gl.public.write
    def request_access(self, resource_id: u256, evidence_url: str) -> u256:
        assert resource_id in self.resources, "Resource not found"
        requester = str(gl.message.sender_address)
        assert f"{int(resource_id)}:{requester}" not in self.grants, "Access already granted"

        cleaned = clean_url(evidence_url)
        assert cleaned is not None, f"Invalid evidence URL: {evidence_url}"
        assert is_valid_url(cleaned), f"Invalid evidence URL: {cleaned}"

        qid = self.next_request_id
        self.next_request_id += u256(1)
        self.requests[qid] = AccessRequest(
            request_id=qid,
            resource_id=resource_id,
            requester=requester,
            evidence_url=cleaned,
            meets_policy=False,
            evidence_relevant=False,
            decision="PENDING",
        )
        return qid

    @gl.public.write
    def decide_access(self, request_id: u256) -> bool:
        assert request_id in self.requests, "Request not found"
        req = self.requests[request_id]
        assert req.decision == "PENDING", "Already decided"

        policy = self.resources[req.resource_id].policy
        evidence_url = req.evidence_url

        # Equivalence Principle: COMPARATIVE, two-field. The contract itself
        # fetches the requester's evidence page; nothing caller-written is judged.
        def leader_fn():
            return assess_access(evidence_url, policy)

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            leader_data = leader_result.calldata
            for field in ("meets_policy", "evidence_relevant"):
                if not isinstance(leader_data.get(field), bool):
                    return False
            mine = assess_access(evidence_url, policy)
            return (
                mine["meets_policy"] == leader_data["meets_policy"]
                and mine["evidence_relevant"] == leader_data["evidence_relevant"]
            )

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        granted = result["meets_policy"] and result["evidence_relevant"]
        req.meets_policy = result["meets_policy"]
        req.evidence_relevant = result["evidence_relevant"]
        req.decision = "GRANTED" if granted else "DENIED"
        self.requests[request_id] = req

        if granted:
            self.grants[f"{int(req.resource_id)}:{req.requester}"] = u256(1)
        return True

    @gl.public.view
    def has_access(self, resource_id: u256, agent: str) -> str:
        if f"{int(resource_id)}:{agent}" in self.grants:
            return "GRANTED"
        return "NO_ACCESS"

    @gl.public.view
    def get_resource_data(self, resource_id: u256) -> str:
        if resource_id not in self.resources:
            return "NOT_FOUND"
        r = self.resources[resource_id]
        return json.dumps({
            "resource_id": int(r.resource_id),
            "owner": r.owner,
            "name": r.name,
            "policy": r.policy,
        })

    @gl.public.view
    def get_request_data(self, request_id: u256) -> str:
        if request_id not in self.requests:
            return "NOT_FOUND"
        q = self.requests[request_id]
        return json.dumps({
            "request_id": int(q.request_id),
            "resource_id": int(q.resource_id),
            "requester": q.requester,
            "evidence_url": q.evidence_url,
            "meets_policy": q.meets_policy,
            "evidence_relevant": q.evidence_relevant,
            "decision": q.decision,
        })

    @gl.public.view
    def list_requests(self) -> str:
        items = []
        for key in self.requests:
            q = self.requests[key]
            items.append(f"{int(q.request_id)}:{q.decision}")
        return ",".join(items)
