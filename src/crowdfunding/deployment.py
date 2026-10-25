from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from solcx import compile_source, get_installed_solc_versions, install_solc
from web3 import EthereumTesterProvider, Web3

from .config import CONTRACT_PATH, SOLC_VERSION


@dataclass
class CrowdfundingDemo:
    w3: Web3
    contract: Any
    owner: str
    contributor: str


def install_solc_version(version: str = SOLC_VERSION) -> None:
    installed_versions = {str(v) for v in get_installed_solc_versions()}
    if version in installed_versions:
        return

    try:
        install_solc(version)
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(
            f"Unable to install Solidity compiler {version}. Ensure network access is available or a local compiler is configured."
        ) from exc


def compile_and_deploy_contract(w3: Web3, deployer: Optional[str] = None) -> Any:
    """Compile the Solidity contract and deploy it to the given Web3 provider."""
    contract_source = CONTRACT_PATH.read_text(encoding="utf-8")
    install_solc_version()

    compiled = compile_source(contract_source, solc_version=SOLC_VERSION)
    _, contract_interface = compiled.popitem()

    contract = w3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])
    tx_hash = contract.constructor().transact({"from": deployer or w3.eth.accounts[0]})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return w3.eth.contract(address=receipt.contractAddress, abi=contract_interface["abi"])


def deploy_test_contract() -> CrowdfundingDemo:
    """Create a local Ethereum test instance with a funded owner and contributor."""
    w3 = Web3(EthereumTesterProvider())
    owner = w3.eth.accounts[0]
    contributor = w3.eth.accounts[1]
    contract = compile_and_deploy_contract(w3, owner)
    return CrowdfundingDemo(w3=w3, contract=contract, owner=owner, contributor=contributor)


def advance_time(w3: Web3, seconds: int) -> None:
    """Advance the Ethereum tester clock by the requested number of seconds."""
    current_block = w3.eth.get_block("latest")
    target_timestamp = current_block["timestamp"] + int(seconds)

    if hasattr(w3.provider, "ethereum_tester"):
        w3.provider.ethereum_tester.time_travel(target_timestamp)
    else:
        w3.provider.make_request("evm_set_next_block_timestamp", [target_timestamp])
        w3.provider.make_request("evm_mine", [])
