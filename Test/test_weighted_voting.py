import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0xd4eB31737d857eB94f75b264F133B1c3e5FB191f"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_only_proposer_can_open_voting(client, non_proposer_client):
    with pytest.raises(Exception, match="Only the proposer can open voting"):
        _write(non_proposer_client, "open_voting", [0])


def test_invalid_support_rejected(client):
    _write(client, "open_voting", [0])
    with pytest.raises(Exception, match="Support must be FOR or AGAINST"):
        _write(client, "cast_vote", [0, "MAYBE"])


def test_zero_power_voter_rejected(client, zero_reputation_client):
    with pytest.raises(Exception, match="No voting power"):
        _write(zero_reputation_client, "cast_vote", [0, "FOR"])


def test_cast_and_close(client, weighted_client):
    """weighted_client belongs to an address with reputation above 50."""
    _write(weighted_client, "cast_vote", [0, "FOR"])
    with pytest.raises(Exception, match="Already voted"):
        _write(weighted_client, "cast_vote", [0, "AGAINST"])
    data = json.loads(_read(client, "get_voting_data", [0]))
    assert data["for_weight"] > 0
    _write(client, "close_voting", [0])
    assert json.loads(_read(client, "get_voting_data", [0]))["status"] == "CLOSED"
