# Ethereum Crowdfunding Smart Contract Demo

This repository contains a small, local Ethereum crowdfunding prototype implemented as a Solidity smart contract and deployed through Python and Web3.py. The project demonstrates the core crowdfunding lifecycle: creating a campaign, accepting contributions, withdrawing funds after a successful round, and refunding supporters if the goal is not reached.

## Overview

The project is intended as a learning-focused demonstration rather than a production-grade DeFi application. It uses an in-memory Ethereum test chain so the contract can be compiled and exercised locally without requiring a live blockchain.

## Why this project exists

Crowdfunding contracts are one of the simplest and most instructive examples of blockchain-based programmable finance. They show how on-chain state, ownership constraints, financial logic, and event emission can be combined to model a funding round.

## Features

- Campaign creation with a title, goal, and deadline
- Contributions in Ether from arbitrary addresses
- Owner-only withdrawal after the deadline when the goal is met
- Contributor refunds after the deadline when the goal is not met
- Event emission for campaign creation, funding, withdrawal, and refund operations
- Local deployment using the Ethereum tester provider for reproducible demos

## Project structure

```text
ethereum-crowdfunding/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── soc_crowdfunding.py
├── contracts/
│   └── Crowdfunding.sol
├── src/
│   └── crowdfunding/
│       ├── __init__.py
│       ├── config.py
│       └── deployment.py
├── scripts/
│   ├── __init__.py
│   └── demo.py
├── tests/
│   └── test_contract_lifecycle.py
└── .github/
    └── workflows/
        └── ci.yml
```

## Smart contract logic

The Solidity contract stores campaign metadata and per-user contributions in a mapping. The main state transitions are:

1. `createCampaign` creates a new campaign with a goal and deadline.
2. `contribute` accepts Ether for an active campaign before the deadline.
3. `withdrawFunds` allows the campaign owner to receive the total raised amount only when the goal is reached and the deadline has passed.
4. `refund` allows any contributor to recover their contribution if the campaign misses its goal by the deadline.

The contract uses a reentrancy guard (`locked`) to guard withdrawal and refund operations.

## Installation

Use Python 3.9 or newer and install the project dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or .venv\Scripts\activate  # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the demo

From the repository root:

```bash
python soc_crowdfunding.py
```

This script deploys a local contract, creates a campaign, accepts a contribution, advances time, and demonstrates the refund flow.

## Running tests

```bash
pytest -q
```

## Validation notes

The project is designed to run on an Ethereum test provider. It does not require a public RPC endpoint or external wallet configuration. The local execution remains isolated to the machine running the demo.

## Limitations

- This is a learning prototype and not intended for production deployment.
- It is not audited for security-critical use.
- The reentrancy guard is simple and contract-level, suitable for a demo rather than a production-grade crowdfunding platform.
- There is no frontend, database, or persisted wallet integration.

## Technologies used

- Solidity
- Python
- Web3.py
- py-solc-x
- eth-tester
- pytest

## License

This project is distributed under the MIT License, unless you choose to add a different one explicitly.
