import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0xA34b809602EA1E42F081AA36a6247A6fC7cde7bb"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_panel_needs_at_least_two(client):
    with pytest.raises(Exception, match="A panel needs at least 2 judgments"):
        _write(client, "score_panel", ["0"])


def test_panel_rejects_duplicate_ids(client):
    with pytest.raises(Exception, match="Duplicate question id in panel"):
        _write(client, "score_panel", ["0,0"])


def test_score_panel(client):
    """Assumes questions 0,1,2 from test_ambiguity_oracle.py (same statement) are judged."""
    _write(client, "score_panel", ["0,1,2"])
    data = json.loads(_read(client, "get_panel_data", [0]))
    total = data["true_count"] + data["false_count"] + data["ambiguous_count"]
    assert total == 3
    assert 0 <= data["dissensus_score"] <= 100


def test_cannot_score_same_panel_twice(client):
    with pytest.raises(Exception, match="Panel already scored"):
        _write(client, "score_panel", ["2,1,0"])
