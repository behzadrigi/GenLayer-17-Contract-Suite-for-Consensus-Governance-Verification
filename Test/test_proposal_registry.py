import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x9e4b7Af1FcA914885856d4d931dF4faAcEF838b1"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_empty_title_rejected(client):
    with pytest.raises(Exception, match="Title cannot be empty"):
        _write(client, "create_proposal", ["", "desc"])


def test_create_proposal(client, sender_address):
    _write(client, "create_proposal", ["Adopt policy X", "Adopt the new contribution policy"])
    data = json.loads(_read(client, "get_proposal_data", [0]))
    assert data["proposer"] == sender_address
