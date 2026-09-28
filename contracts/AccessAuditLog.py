# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json

from genlayer import *
from dataclasses import dataclass


@allow_storage
@dataclass
class LogEntry:
    log_id: u256
    request_id: u256
    resource_id: u256
    requester: str
    decision: str


class AccessAuditLog(gl.Contract):
    entries: TreeMap[u256, LogEntry]
    logged_requests: TreeMap[u256, u256]
    next_id: u256
    gate_contract: str

    def __init__(self, gate_address: str):
        self.next_id = u256(0)
        self.gate_contract = gate_address

    @gl.public.write
    def record_decision(self, request_id: u256) -> u256:
        assert request_id not in self.logged_requests, "Decision already logged"

        raw = gl.get_contract_at(
            Address(self.gate_contract)
        ).view().get_request_data(request_id)
        assert raw != "NOT_FOUND", "Request not found in gate"

        try:
            data = json.loads(raw)
        except:
            raise gl.vm.UserError("Invalid data from gate")

        decision = data.get("decision", "")
        assert decision in ("GRANTED", "DENIED"), "Request has not been decided yet"

        lid = self.next_id
        self.next_id += u256(1)

        self.entries[lid] = LogEntry(
            log_id=lid,
            request_id=request_id,
            resource_id=u256(int(data.get("resource_id", 0))),
            requester=data.get("requester", ""),
            decision=decision,
        )
        self.logged_requests[request_id] = u256(1)
        return lid

    @gl.public.view
    def get_log_data(self, log_id: u256) -> str:
        if log_id not in self.entries:
            return "NOT_FOUND"
        e = self.entries[log_id]
        return json.dumps({
            "log_id": int(e.log_id),
            "request_id": int(e.request_id),
            "resource_id": int(e.resource_id),
            "requester": e.requester,
            "decision": e.decision,
        })

    @gl.public.view
    def get_agent_logs(self, agent: str) -> str:
        items = []
        for key in self.entries:
            e = self.entries[key]
            if e.requester == agent:
                items.append(f"{int(e.log_id)}:{e.decision}")
        return ",".join(items)

    @gl.public.view
    def get_resource_logs(self, resource_id: u256) -> str:
        items = []
        for key in self.entries:
            e = self.entries[key]
            if e.resource_id == resource_id:
                items.append(f"{int(e.log_id)}:{e.decision}")
        return ",".join(items)

    @gl.public.view
    def list_logs(self) -> str:
        items = []
        for key in self.entries:
            e = self.entries[key]
            items.append(f"{int(e.log_id)}:{e.decision}")
        return ",".join(items)
