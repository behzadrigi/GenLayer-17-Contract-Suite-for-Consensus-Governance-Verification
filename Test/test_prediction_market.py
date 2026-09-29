import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x878aF3a632E28cbE14E4a87e83897FD3e98DBd84"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_only_deployer_can_set_oracle(client, non_deployer_client):
    with pytest.raises(Exception, match="Only deployer can set the oracle"):
        _write(non_deployer_client, "set_oracle", ["0x0000000000000000000000000000000000000000"])


def test_claim_points_once(client, agent_address):
    _write(client, "claim_points", [])
    assert _read(client, "get_balance", [agent_address]) == "BALANCE:100"
    with pytest.raises(Exception, match="Points already claimed"):
        _write(client, "claim_points", [])


def test_create_market_invalid_url(client):
    with pytest.raises(Exception, match="Invalid source URL"):
        _write(client, "create_market", ["q", "not_a_url"])


def test_full_market_cycle(client, agent_address):
    _write(client, "create_market", [
        "Is Python a programming language?", "https://www.python.org/about",
    ])
    market_id = 0
    _write(client, "place_bet", [market_id, "YES", 30])
    with pytest.raises(Exception, match="Side must be YES or NO"):
        _write(client, "place_bet", [market_id, "MAYBE", 5])
    with pytest.raises(Exception, match="Insufficient points"):
        _write(client, "place_bet", [market_id, "YES", 100000])

    with pytest.raises(Exception, match="Market must be closed before settlement"):
        _write(client, "settle_market", [market_id])

    _write(client, "close_market", [market_id])
    with pytest.raises(Exception, match="Market is not open for bets"):
        _write(client, "place_bet", [market_id, "YES", 5])
    with pytest.raises(Exception, match="No resolution found in oracle"):
        _write(client, "settle_market", [market_id])
