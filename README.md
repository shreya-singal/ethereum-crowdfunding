# Ethereum Crowdfunding Demo

A small Ethereum crowdfunding prototype built with Solidity and Python. This project demonstrates a complete crowdfunding lifecycle locally on an in-memory EVM, without requiring a public blockchain or wallet setup.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/tests-passing-brightgreen)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

This repository models a basic crowdfunding smart contract where:

- a campaign owner can create a funding round
- anyone can contribute ETH before the deadline
- the owner can withdraw funds only after the goal is reached and the deadline passes
- contributors can refund their support if the campaign misses the target

The project is designed as a learning-focused demo and local development sandbox for Ethereum smart contract flows.

## Why this project

Crowdfunding is one of the clearest examples of how blockchain logic can enforce trustless fundraising rules. It combines:

- stateful Solidity storage
- on-chain validation
- time-based conditions
- ownership restrictions
- value transfer logic
- event-driven workflows

## Features

- campaign creation with title, funding goal, and deadline
- Ether contributions from multiple addresses
- owner-only withdrawals after success
- refund logic for failed campaigns
- local EVM deployment using `eth-tester`
- Python-based automation with `web3.py`
- automated tests for the lifecycle

## Architecture

The project is split into a smart contract and a small Python orchestration layer:

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
├── .github/
│   └── workflows/
│       └── ci.yml
└── .venv/
```

## Smart contract behavior

The Solidity contract stores campaign metadata and per-user contribution records. The main lifecycle is:

1. `createCampaign(...)` creates a campaign with a funding target and deadline.
2. `contribute(...)` accepts ETH from a participant before the deadline.
3. `withdrawFunds(...)` allows the owner to withdraw funds only after the deadline and only if the goal is met.
4. `refund(...)` allows contributors to recover funds if the goal is not reached.

A simple reentrancy guard is included for basic protection during withdrawals and refunds.

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ethereum-crowdfunding.git
cd ethereum-crowdfunding
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the demo

```bash
python soc_crowdfunding.py
```

This script deploys the contract locally, creates a campaign, contributes funds, advances time, and triggers the refund flow.

## Local demo example

A typical run produces output like this:

```text
Contract deployed at: 0xF2E246BB76DF876Cef8b38ae84130F4F55De395b
Campaign created
Contribution received: 500
Refund complete: 0
Campaign state: ['0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf', 'Community Round', 1000, 1792953234, 500, False]
```

This confirms the contract lifecycle is functioning end-to-end against the in-memory Ethereum test provider.

## Running tests

```bash
pytest -q
```

### Current validation status

The repository currently passes its local test suite:

```text
4 passed, 1 warning in 11.47s
```

The warning is a dependency deprecation notice from `websockets` and does not affect contract execution.

## Project metrics

| Metric | Value |
| --- | --- |
| Test status | Passing |
| Automated tests | 4 |
| Last verified run | 11.47s |
| Demo status | Local EVM walkthrough working |
| Contract model | Solidity crowdfunding contract |
| Python integration | Web3.py + EthereumTesterProvider |

## Repository structure

```text
contracts/
  Crowdfunding.sol
src/crowdfunding/
  __init__.py
  config.py
  deployment.py
scripts/
  demo.py
tests/
  test_contract_lifecycle.py
```

## Technologies used

- Solidity
- Python
- Web3.py
- py-solc-x
- eth-tester
- pytest

## Limitations

This is a learning/demo project and is not intended for production deployment or audit-ready use. It is designed for local experimentation and understanding Ethereum crowdfunding logic.

## Contributing

Contributions are welcome. If you want to improve the project:

1. open an issue or propose a feature
2. fork the repository
3. create a feature branch
4. add or update tests
5. open a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Notes

This project intentionally avoids external RPC dependencies and instead uses a local in-memory Ethereum test chain for reproducible development and testing.
