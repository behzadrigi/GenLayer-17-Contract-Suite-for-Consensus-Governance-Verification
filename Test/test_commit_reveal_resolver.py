import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x088457276DD013804C9655fB99CfD0C9B17d7d0C"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_finalize_requires_positive_quorum(client):
    with pytest.raises(Exception, match="min_reveals must be positive"):
        _write(client, "finalize_poll", [0, 0])


def test_finalize_nonexistent_poll(client):
    with pytest.raises(Exception, match="Poll not found in vote contract"):
        _write(client, "finalize_poll", [999, 1])


def test_cannot_finalize_twice(client):
    """Assumes poll 0 from test_commit_reveal_vote.py is CLOSED with 1 reveal."""
    _write(client, "finalize_poll", [0, 1])
    with pytest.raises(Exception, match="Poll already finalized"):
        _write(client, "finalize_poll", [0, 1])
