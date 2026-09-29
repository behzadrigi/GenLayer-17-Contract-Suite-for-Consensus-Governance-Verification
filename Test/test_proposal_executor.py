import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x108386Ad959881d2c3B89474B41C3cF6218DD5AD"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_quorum_not_met(client):
    with pytest.raises(Exception, match="Quorum not met"):
        _write(client, "execute_proposal", [0, 100000])


def test_min_total_weight_must_be_positive(client):
    with pytest.raises(Exception, match="min_total_weight must be positive"):
        _write(client, "execute_proposal", [0, 0])


def test_execute_proposal(client):
    """Assumes voting on proposal 0 from test_weighted_voting.py is CLOSED."""
    outcome = _write(client, "execute_proposal", [0, 1])
    data = json.loads(_read(client, "get_execution_data", [0]))
    assert data["outcome"] in ("PASSED", "REJECTED")
    with pytest.raises(Exception, match="Proposal already executed"):
        _write(client, "execute_proposal", [0, 1])
