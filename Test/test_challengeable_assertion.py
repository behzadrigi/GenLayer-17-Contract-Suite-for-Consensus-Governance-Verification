import json
import pytest
from genlayer_py import create_client, create_account
from genlayer_py.chains import localnet

CONTRACT_ADDRESS = "0xEd570624974Df028B0bd447526d363ad0B26c898"


@pytest.fixture(scope="module")
def client():
    return create_client(chain=localnet, account=create_account())


def _write(client, fn, args):
    tx = client.write_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args, value=0)
    return client.wait_for_transaction_receipt(transaction_hash=tx, status="ACCEPTED")


def _read(client, fn, args=None):
    return client.read_contract(address=CONTRACT_ADDRESS, function_name=fn, args=args or [])


def test_assert_claim_validation(client):
    with pytest.raises(Exception, match="Statement cannot be empty"):
        _write(client, "assert_claim", ["", "https://en.wikipedia.org/wiki/Guido_van_Rossum"])
    with pytest.raises(Exception, match="Invalid evidence URL"):
        _write(client, "assert_claim", ["x", "not_a_url"])


def test_evaluate_and_challenge_flow(client, challenger_client, challenger_address):
    _write(client, "assert_claim", [
        "Python was created by Guido van Rossum",
        "https://en.wikipedia.org/wiki/Guido_van_Rossum",
    ])
    assertion_id = 0

    with pytest.raises(Exception, match="Only an accepted assertion can be challenged"):
        _write(challenger_client, "challenge", [assertion_id, "https://www.python.org/about"])

    _write(client, "evaluate", [assertion_id])
    data = json.loads(_read(client, "get_assertion_data", [assertion_id]))
    assert data["status"] in ("ACCEPTED", "REJECTED")

    with pytest.raises(Exception, match="Assertion already evaluated"):
        _write(client, "evaluate", [assertion_id])

    if data["status"] == "ACCEPTED":
        with pytest.raises(Exception, match="Asserter cannot challenge their own assertion"):
            _write(client, "challenge", [assertion_id, "https://www.python.org/about"])
        with pytest.raises(Exception, match="Counter-evidence must differ from the original evidence"):
            _write(challenger_client, "challenge", [
                assertion_id, "https://en.wikipedia.org/wiki/Guido_van_Rossum",
            ])
        _write(challenger_client, "challenge", [assertion_id, "https://www.python.org/about"])
        result = json.loads(_read(client, "get_assertion_data", [assertion_id]))
        assert result["status"] == "CHALLENGED"
        assert result["challenger"] == challenger_address
