import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x74FDE232d4a410C07dd31f8394beAD8DE38dCF4E"
LABELS = ("TRUE", "FALSE", "AMBIGUOUS")


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_invalid_source_url_rejected(client):
    with pytest.raises(Exception, match="Invalid source URL"):
        _write(client, "submit_statement", ["Python was created by Guido van Rossum", "not_a_url"])


def test_judge_question(client):
    _write(client, "submit_statement", [
        "Python was created by Guido van Rossum",
        "https://en.wikipedia.org/wiki/Guido_van_Rossum",
    ])
    question_id = 0
    _write(client, "judge_question", [question_id])
    data = json.loads(_read(client, "get_judgment_data", [question_id]))
    assert data["label"] in LABELS
    assert data["status"] == "JUDGED"


def test_cannot_judge_twice(client):
    with pytest.raises(Exception, match="Already judged"):
        _write(client, "judge_question", [0])


def test_judge_nonexistent_question(client):
    with pytest.raises(Exception, match="Question not found"):
        _write(client, "judge_question", [999])
