import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x188cDB8a68afA42Af3FadCEF3687452A890B9d65"
VERDICTS = ("VALID", "INVALID", "INCOMPLETE")


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_check_proof(client):
    """Assumes proof 0 from test_proof_registry.py exists."""
    _write(client, "check_proof", [0])
    data = json.loads(_read(client, "get_check_data", [0]))
    assert data["verdict"] in VERDICTS
    assert data["status"] == "CHECKED"


def test_cannot_check_twice(client):
    with pytest.raises(Exception, match="Already checked"):
        _write(client, "check_proof", [0])


def test_check_nonexistent_proof(client):
    with pytest.raises(Exception, match="Proof not found in registry"):
        _write(client, "check_proof", [999])
