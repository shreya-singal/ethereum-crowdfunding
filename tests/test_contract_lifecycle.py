import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crowdfunding.deployment import advance_time, deploy_test_contract


@pytest.fixture
def demo_contract():
    return deploy_test_contract()


def test_campaign_creation_and_contribution(demo_contract):
    contract = demo_contract.contract
    owner = demo_contract.owner
    contributor = demo_contract.contributor

    tx_hash = contract.functions.createCampaign("Launchpad", 1_000, 10).transact({"from": owner})
    demo_contract.w3.eth.wait_for_transaction_receipt(tx_hash)

    tx_hash = contract.functions.contribute(0).transact({"from": contributor, "value": 500})
    demo_contract.w3.eth.wait_for_transaction_receipt(tx_hash)

    campaign = contract.functions.getCampaign(0).call()
    contribution = contract.functions.getContribution(0, contributor).call()

    assert campaign[2] == 1_000
    assert campaign[4] == 500
    assert contribution == 500


def test_refund_when_goal_is_not_met(demo_contract):
    contract = demo_contract.contract
    owner = demo_contract.owner
    contributor = demo_contract.contributor
    w3 = demo_contract.w3

    tx_hash = contract.functions.createCampaign("Kickstarter", 1_000, 10).transact({"from": owner})
    w3.eth.wait_for_transaction_receipt(tx_hash)

    tx_hash = contract.functions.contribute(0).transact({"from": contributor, "value": 250})
    w3.eth.wait_for_transaction_receipt(tx_hash)

    advance_time(w3, 11)

    tx_hash = contract.functions.refund(0).transact({"from": contributor})
    w3.eth.wait_for_transaction_receipt(tx_hash)

    assert contract.functions.getContribution(0, contributor).call() == 0
    assert contract.functions.getCampaign(0).call()[4] == 250


def test_owner_can_withdraw_after_goal_is_met(demo_contract):
    contract = demo_contract.contract
    owner = demo_contract.owner
    contributor = demo_contract.contributor
    w3 = demo_contract.w3

    tx_hash = contract.functions.createCampaign("FullFunding", 1_000, 10).transact({"from": owner})
    w3.eth.wait_for_transaction_receipt(tx_hash)

    tx_hash = contract.functions.contribute(0).transact({"from": contributor, "value": 1_000})
    w3.eth.wait_for_transaction_receipt(tx_hash)

    advance_time(w3, 11)

    tx_hash = contract.functions.withdrawFunds(0).transact({"from": owner})
    w3.eth.wait_for_transaction_receipt(tx_hash)

    campaign = contract.functions.getCampaign(0).call()
    assert campaign[5] is True
    assert campaign[4] == 1_000
