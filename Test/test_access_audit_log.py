import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x64d695F0a53a2ac4aa194126D744378956C4b230"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_record_decision(client):
    """Assumes request 0 from test_semantic_access_gate.py has been decided."""
    _write(client, "record_decision", [0])
    listing = _read(client, "list_logs")
    assert "0:" in listing


def test_cannot_log_twice(client):
    with pytest.raises(Exception, match="Decision already logged"):
        _write(client, "record_decision", [0])


def test_log_nonexistent_request(client):
    with pytest.raises(Exception, match="Request not found in gate"):
        _write(client, "record_decision", [999])
