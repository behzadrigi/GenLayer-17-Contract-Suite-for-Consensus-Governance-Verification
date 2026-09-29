import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x6E69DfD4a8e8B061cB1A4cF0E134170a8f6bD035"
OUTCOMES = ("YES", "NO", "UNRESOLVED")


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_resolve_open_market_rejected(client):
    with pytest.raises(Exception, match="Market must be closed before resolution"):
        _write(client, "resolve_market", [1])  # a still-open market in the deployment


def test_resolve_market(client):
    """Assumes market 0 from test_prediction_market.py has been closed."""
    _write(client, "resolve_market", [0])
    data = json.loads(_read(client, "get_resolution_data", [0]))
    assert data["outcome"] in OUTCOMES
    with pytest.raises(Exception, match="Market already resolved"):
        _write(client, "resolve_market", [0])


def test_resolve_nonexistent_market(client):
    with pytest.raises(Exception, match="Market not found"):
        _write(client, "resolve_market", [999])
