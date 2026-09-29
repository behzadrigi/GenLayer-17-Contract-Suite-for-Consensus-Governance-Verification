import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0xeBbe5c528854443e0aAE9eC83a4abbd075f9ea6F"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_lazy_default_reputation(client, some_address):
    assert _read(client, "get_reputation", [some_address]) == "REPUTATION:50"


def test_not_enough_epochs_observed(client, fresh_agent_address):
    with pytest.raises(Exception, match="Not enough epochs observed"):
        _write(client, "apply_liveness", [fresh_agent_address])


def test_unregistered_service_rejected(client, unregistered_address):
    with pytest.raises(Exception, match="Service not found in monitor"):
        _write(client, "apply_liveness", [unregistered_address])


def test_apply_liveness(client, agent_address_with_3_epochs):
    """Assumes an agent from test_service_heartbeat_monitor.py has >=3 epochs observed."""
    _write(client, "apply_liveness", [agent_address_with_3_epochs])
    data = json.loads(_read(client, "get_change_details", [0]))
    assert data["agent"] == agent_address_with_3_epochs
    assert data["change_type"] in ("INCREASE", "DECREASE")
    with pytest.raises(Exception, match="Already applied for this observation count"):
        _write(client, "apply_liveness", [agent_address_with_3_epochs])
