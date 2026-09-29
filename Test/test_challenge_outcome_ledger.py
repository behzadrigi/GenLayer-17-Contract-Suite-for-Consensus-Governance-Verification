import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0xe552B9C3cdb79fD4F6E8D1E36973327075ba2D46"
FINAL_STATUSES = ("FINALIZED_ACCEPTED", "FINALIZED_OVERTURNED", "REJECTED")


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_record_pending_assertion_rejected(client):
    with pytest.raises(Exception, match="Assertion has not reached a final status"):
        _write(client, "record_outcome", [some_pending_id := 2])


def test_record_nonexistent_assertion(client):
    with pytest.raises(Exception, match="Assertion not found"):
        _write(client, "record_outcome", [999])


def test_record_outcome(client, asserter_address):
    """Assumes assertion 1 (REJECTED) from the full suite test run exists."""
    _write(client, "record_outcome", [1])
    data = json.loads(_read(client, "get_outcome_data", [1]))
    assert data["final_status"] in FINAL_STATUSES
    record = json.loads(_read(client, "get_agent_record", [asserter_address]))
    assert record["upheld"] + record["lost"] >= 1
    with pytest.raises(Exception, match="Outcome already recorded"):
        _write(client, "record_outcome", [1])
