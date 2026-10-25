from __future__ import annotations

from crowdfunding.deployment import CrowdfundingDemo, advance_time, deploy_test_contract


def main() -> None:
    demo = deploy_test_contract()
    contract = demo.contract
    owner = demo.owner
    contributor = demo.contributor

    print("Contract deployed at:", contract.address)

    tx_hash = contract.functions.createCampaign("Community Round", 1_000, 10).transact({"from": owner})
    demo.w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Campaign created")

    tx_hash = contract.functions.contribute(0).transact({"from": contributor, "value": 500})
    demo.w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Contribution received:", contract.functions.getContribution(0, contributor).call())

    advance_time(demo.w3, 11)
    tx_hash = contract.functions.refund(0).transact({"from": contributor})
    demo.w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Refund complete:", contract.functions.getContribution(0, contributor).call())

    print("Campaign state:", contract.functions.getCampaign(0).call())


if __name__ == "__main__":
    main()
