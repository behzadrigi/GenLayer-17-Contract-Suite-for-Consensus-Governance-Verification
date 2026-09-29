import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x09bcbCCD0F128aB29ddC9228aF737D37F1623b91"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_register_resource_requires_name_and_policy(client):
    with pytest.raises(Exception, match="Name cannot be empty"):
        _write(client, "register_resource", ["", "policy"])
    with pytest.raises(Exception, match="Policy cannot be empty"):
        _write(client, "register_resource", ["name", ""])


def test_full_access_decision(client, requester_address):
    _write(client, "register_resource", [
        "Python Guild Repo",
        "Requester must demonstrate published, verifiable experience with the Python programming language",
    ])
    resource_id = 0
    _write(client, "request_access", [resource_id, "https://en.wikipedia.org/wiki/Guido_van_Rossum"])
    request_id = 0
    _write(client, "decide_access", [request_id])
    data = json.loads(_read(client, "get_request_data", [request_id]))
    assert data["decision"] in ("GRANTED", "DENIED")
    if data["decision"] == "GRANTED":
        assert _read(client, "has_access", [resource_id, requester_address]) == "GRANTED"


def test_cannot_decide_twice(client):
    with pytest.raises(Exception, match="Already decided"):
        _write(client, "decide_access", [0])


def test_invalid_evidence_url_rejected(client):
    with pytest.raises(Exception, match="Invalid evidence URL"):
        _write(client, "request_access", [0, "not_a_url"])
