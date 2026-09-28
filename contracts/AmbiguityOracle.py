# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
import re

from genlayer import *
from dataclasses import dataclass

LABELS = ("TRUE", "FALSE", "AMBIGUOUS")


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


def judge_statement(statement: str, source_url: str) -> str:
    try:
        content = gl.nondet.web.render(source_url)
    except:
        return "AMBIGUOUS"
    if content.strip() == "":
        return "AMBIGUOUS"

    prompt = f"""
    Statement: {statement}

    Source content ({source_url}):
    {content[:2500]}

    Based ONLY on this source, is the statement TRUE, FALSE, or AMBIGUOUS
    (the source is silent, unclear, or contains conflicting information)?
    Respond with ONLY one word: TRUE, FALSE, or AMBIGUOUS.
    """
    response = gl.nondet.exec_prompt(prompt)
    return first_label(response, LABELS, "AMBIGUOUS")


@allow_storage
@dataclass
class QuestionRecord:
    question_id: u256
    asker: str
    statement: str
    source_url: str
    label: str
    status: str  # PENDING, JUDGED


class AmbiguityOracle(gl.Contract):
    questions: TreeMap[u256, QuestionRecord]
    next_id: u256

    def __init__(self):
        self.next_id = u256(0)

    @gl.public.write
    def submit_statement(self, statement: str, source_url: str) -> u256:
        assert statement.strip() != "", "Statement cannot be empty"
        cleaned = clean_url(source_url)
        assert cleaned is not None, f"Invalid source URL: {source_url}"
        assert is_valid_url(cleaned), f"Invalid source URL: {cleaned}"

        qid = self.next_id
        self.next_id += u256(1)

        self.questions[qid] = QuestionRecord(
            question_id=qid,
            asker=str(gl.message.sender_address),
            statement=statement,
            source_url=cleaned,
            label="",
            status="PENDING",
        )
        return qid

    @gl.public.write
    def judge_question(self, question_id: u256) -> bool:
        assert question_id in self.questions, "Question not found"
        q = self.questions[question_id]
        assert q.status == "PENDING", "Already judged"

        statement = q.statement
        source_url = q.source_url

        # Equivalence Principle: STRICT EQUALITY on a three-way label.
        def leader_fn():
            return {"label": judge_statement(statement, source_url)}

        def validator_fn(leader_result):
            if not isinstance(leader_result, gl.vm.Return):
                return False
            leader_label = leader_result.calldata.get("label")
            if leader_label not in LABELS:
                return False
            return judge_statement(statement, source_url) == leader_label

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        q.label = result["label"]
        q.status = "JUDGED"
        self.questions[question_id] = q
        return True

    @gl.public.view
    def get_judgment_data(self, question_id: u256) -> str:
        if question_id not in self.questions:
            return "NOT_FOUND"
        q = self.questions[question_id]
        return json.dumps({
            "question_id": int(q.question_id),
            "asker": q.asker,
            "statement": q.statement,
            "source_url": q.source_url,
            "label": q.label,
            "status": q.status,
        })

    @gl.public.view
    def list_questions(self) -> str:
        items = []
        for key in self.questions:
            q = self.questions[key]
            items.append(f"{int(q.question_id)}:{q.status}:{q.label}")
        return ",".join(items)
