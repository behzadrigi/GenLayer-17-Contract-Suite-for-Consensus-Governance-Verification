import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0x3cC830503F9E660b658f04A6131ce5826e8d8eA3"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_only_admin_can_advance_epoch(client, non_admin_client):
    with pytest.raises(Exception, match="Only admin can advance the epoch"):
        _write(non_admin_client, "advance_epoch", [])


def test_register_and_heartbeat(client, agent_address):
    _write(client, "register_service", ["service-b"])
    data = json.loads(_read(client, "get_service_data", [agent_address]))
    assert data["status"] == "ACTIVE"
    assert data["total_beats"] == 1
    with pytest.raises(Exception, match="Already sent a heartbeat this epoch"):
        _write(client, "heartbeat", [])


def test_cannot_register_twice(client):
    with pytest.raises(Exception, match="Service already registered"):
        _write(client, "register_service", ["again"])


def test_missed_epochs_mark_down(client, agent_address):
    """Advancing two epochs without a heartbeat should mark the service DOWN."""
    _write(client, "advance_epoch", [])
    _write(client, "advance_epoch", [])
    data = json.loads(_read(client, "get_service_data", [agent_address]))
    assert data["consecutive_missed"] >= 2
    assert data["status"] == "DOWN"
