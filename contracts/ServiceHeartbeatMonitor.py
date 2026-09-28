# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json

from genlayer import *
from dataclasses import dataclass


@allow_storage
@dataclass
class ServiceRecord:
    agent: str
    name: str
    status: str  # ACTIVE, DOWN
    total_beats: u256
    total_missed: u256
    consecutive_missed: u256


class ServiceHeartbeatMonitor(gl.Contract):
    services: TreeMap[str, ServiceRecord]
    service_index: TreeMap[u256, str]
    beats: TreeMap[str, u256]
    service_count: u256
    current_epoch: u256
    admin: str

    def __init__(self):
        self.service_count = u256(0)
        self.current_epoch = u256(0)
        self.admin = str(gl.message.sender_address)

    @gl.public.write
    def register_service(self, name: str):
        agent = str(gl.message.sender_address)
        assert name.strip() != "", "Name cannot be empty"
        assert agent not in self.services, "Service already registered"

        self.services[agent] = ServiceRecord(
            agent=agent,
            name=name,
            status="ACTIVE",
            total_beats=u256(1),  # registration counts as the first heartbeat
            total_missed=u256(0),
            consecutive_missed=u256(0),
        )
        self.service_index[self.service_count] = agent
        self.service_count += u256(1)
        self.beats[f"{int(self.current_epoch)}:{agent}"] = u256(1)

    @gl.public.write
    def heartbeat(self):
        agent = str(gl.message.sender_address)
        assert agent in self.services, "Service not registered"

        key = f"{int(self.current_epoch)}:{agent}"
        assert key not in self.beats, "Already sent a heartbeat this epoch"

        svc = self.services[agent]
        svc.total_beats = svc.total_beats + u256(1)
        svc.consecutive_missed = u256(0)
        svc.status = "ACTIVE"
        self.services[agent] = svc
        self.beats[key] = u256(1)

    @gl.public.write
    def advance_epoch(self):
        # Liveness is measured in explicit epochs advanced by the admin, not by
        # wall-clock time, because this SDK version has no block timestamp.
        assert str(gl.message.sender_address) == self.admin, "Only admin can advance the epoch"

        closing = int(self.current_epoch)
        for i in range(int(self.service_count)):
            agent = self.service_index[u256(i)]
            svc = self.services[agent]
            if f"{closing}:{agent}" not in self.beats:
                svc.total_missed = svc.total_missed + u256(1)
                svc.consecutive_missed = svc.consecutive_missed + u256(1)
                if svc.consecutive_missed >= u256(2):
                    svc.status = "DOWN"
                self.services[agent] = svc

        self.current_epoch += u256(1)

    @gl.public.view
    def get_current_epoch(self) -> str:
        return str(int(self.current_epoch))

    @gl.public.view
    def get_service_data(self, agent: str) -> str:
        if agent not in self.services:
            return "NOT_FOUND"
        s = self.services[agent]
        return json.dumps({
            "agent": s.agent,
            "name": s.name,
            "status": s.status,
            "total_beats": int(s.total_beats),
            "total_missed": int(s.total_missed),
            "consecutive_missed": int(s.consecutive_missed),
            "epochs_observed": int(s.total_beats) + int(s.total_missed),
        })

    @gl.public.view
    def list_services(self) -> str:
        items = []
        for i in range(int(self.service_count)):
            agent = self.service_index[u256(i)]
            items.append(f"{agent}:{self.services[agent].status}")
        return ",".join(items)

    @gl.public.view
    def get_admin(self) -> str:
        return self.admin
