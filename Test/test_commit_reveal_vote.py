import hashlib
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0xa88481C105e5d490708c834C8e8fbFf42133aE90"


def commitment(choice, salt):
    return hashlib.sha256(f"{choice}:{salt}".encode()).hexdigest()


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_create_poll_rejects_duplicate_options(client):
    with pytest.raises(Exception, match="Duplicate options"):
        _write(client, "create_poll", ["q", "YES,YES"])


def test_create_poll_requires_two_options(client):
    with pytest.raises(Exception, match="At least 2 options required"):
        _write(client, "create_poll", ["q", "YES"])


def test_full_commit_reveal_cycle(client):
    _write(client, "create_poll", ["Should we merge PR 42?", "YES,NO"])
    poll_id = 0
    _write(client, "commit_vote", [poll_id, commitment("YES", "saltA")])
    with pytest.raises(Exception, match="Poll is not in reveal phase"):
        _write(client, "reveal_vote", [poll_id, "YES", "saltA"])
    _write(client, "advance_to_reveal", [poll_id])
    with pytest.raises(Exception, match="Revealed choice does not match commitment"):
        _write(client, "reveal_vote", [poll_id, "NO", "wrongsalt"])
    _write(client, "reveal_vote", [poll_id, "YES", "saltA"])
    with pytest.raises(Exception, match="Already revealed"):
        _write(client, "reveal_vote", [poll_id, "YES", "saltA"])
    winner = _write(client, "close_poll", [poll_id])
    assert _read(client, "get_tally", [poll_id, "YES"]) == "1"
