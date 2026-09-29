import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x5A81bBCD23004ad553f9caCC4de9cC5F35a9a083"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_empty_statement_rejected(client):
    with pytest.raises(Exception, match="Statement cannot be empty"):
        _write(client, "submit_proof", ["", "https://en.wikipedia.org/wiki/Pythagorean_theorem"])


def test_invalid_url_rejected(client):
    with pytest.raises(Exception, match="Invalid proof URL"):
        _write(client, "submit_proof", ["x", "not_a_url"])


def test_submit_proof(client, sender_address):
    _write(client, "submit_proof", [
        "In a right triangle the square of the hypotenuse equals the sum of the squares of the other two sides",
        "https://en.wikipedia.org/wiki/Pythagorean_theorem",
    ])
    data = json.loads(_read(client, "get_proof_data", [0]))
    assert data["author"] == sender_address
    assert data["status"] == "SUBMITTED"
