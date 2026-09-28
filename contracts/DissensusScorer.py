# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json

from genlayer import *
from dataclasses import dataclass


@allow_storage
@dataclass
class PanelRecord:
    panel_id: u256
    assembler: str
    statement: str
    question_ids: str
    true_count: u256
    false_count: u256
    ambiguous_count: u256
    majority_label: str
    dissensus_score: u256


class DissensusScorer(gl.Contract):
    panels: TreeMap[u256, PanelRecord]
    scored_panels: TreeMap[str, u256]
    next_id: u256
    oracle_contract: str

    def __init__(self, oracle_address: str):
        self.next_id = u256(0)
        self.oracle_contract = oracle_address

    @gl.public.write
    def score_panel(self, question_ids: str) -> u256:
        try:
            ids = [int(x.strip()) for x in question_ids.split(',') if x.strip()]
        except:
            raise gl.vm.UserError("question_ids must be comma-separated integers")

        assert len(ids) >= 2, "A panel needs at least 2 judgments"
        assert len(set(ids)) == len(ids), "Duplicate question id in panel"

        ids = sorted(ids)
        panel_key = ",".join(str(i) for i in ids)
        assert panel_key not in self.scored_panels, "Panel already scored"

        counts = {"TRUE": 0, "FALSE": 0, "AMBIGUOUS": 0}
        statement = ""

        for qid in ids:
            raw = gl.get_contract_at(
                Address(self.oracle_contract)
            ).view().get_judgment_data(u256(qid))
            assert raw != "NOT_FOUND", f"Question {qid} not found in oracle"

            try:
                data = json.loads(raw)
            except:
                raise gl.vm.UserError("Invalid data from oracle")

            assert data.get("status", "") == "JUDGED", f"Question {qid} has not been judged yet"

            if statement == "":
                statement = data.get("statement", "")
            assert data.get("statement", "") == statement, "Panel questions must share the same statement"

            label = data.get("label", "")
            assert label in counts, "Invalid label from oracle"
            counts[label] += 1

        total = len(ids)
        max_count = max(counts.values())
        leaders = [label for label, c in counts.items() if c == max_count]
        majority_label = leaders[0] if len(leaders) == 1 else "SPLIT"
        dissensus = 100 - (max_count * 100) // total

        pid = self.next_id
        self.next_id += u256(1)

        self.panels[pid] = PanelRecord(
            panel_id=pid,
            assembler=str(gl.message.sender_address),
            statement=statement,
            question_ids=panel_key,
            true_count=u256(counts["TRUE"]),
            false_count=u256(counts["FALSE"]),
            ambiguous_count=u256(counts["AMBIGUOUS"]),
            majority_label=majority_label,
            dissensus_score=u256(dissensus),
        )
        self.scored_panels[panel_key] = u256(1)
        return pid

    @gl.public.view
    def get_panel_data(self, panel_id: u256) -> str:
        if panel_id not in self.panels:
            return "NOT_FOUND"
        p = self.panels[panel_id]
        return json.dumps({
            "panel_id": int(p.panel_id),
            "assembler": p.assembler,
            "statement": p.statement,
            "question_ids": p.question_ids,
            "true_count": int(p.true_count),
            "false_count": int(p.false_count),
            "ambiguous_count": int(p.ambiguous_count),
            "majority_label": p.majority_label,
            "dissensus_score": int(p.dissensus_score),
        })

    @gl.public.view
    def list_panels(self) -> str:
        items = []
        for key in self.panels:
            p = self.panels[key]
            items.append(f"{int(p.panel_id)}:{p.majority_label}:{int(p.dissensus_score)}")
        return ",".join(items)
