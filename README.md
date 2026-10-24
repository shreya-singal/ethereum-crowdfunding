# On- Chain Crowdfunding

A decentralized crowdfunding application built using **Solidity, Python, and Web3.py**. The project explores how Ethereum smart contracts can manage fundraising campaigns, contributions, withdrawals, and refunds.

## Features

- **Campaign Creation:** Create fundraising campaigns with a target amount and deadline.
- **Contributions:** Allow users to contribute Ether to active campaigns.
- **Fund Withdrawal:** Enable campaign owners to withdraw funds once the target is met and the deadline has passed.
- **Refunds:** Allow contributors to reclaim their funds if a campaign fails to reach its target.
- **Transparency:** Track campaign details, contributions, and transactions through smart contract functions and events.
- **Security:** Includes a basic reentrancy guard for withdrawal and refund operations.


## How It Works

1. A user creates a campaign with a funding goal and deadline.
2. Contributors send Ether to support the campaign.
3. Once the deadline passes:
   - If the goal is reached, the campaign owner can withdraw the funds.
   - If the goal is not reached, contributors can request refunds.
4. Campaign details and individual contributions can be queried from the smart contract.

## Running the Project

The project was developed and tested using Google Colab with a local Ethereum test environment.

Install the dependencies:

```bash
pip install web3 py-solc-x eth-tester==0.9.0b1 py-evm==0.7.0a2
```

Run the demonstration in Google Colab after installing the dependencies. The supplied script deploys a contract, creates a campaign, makes a contribution, and demonstrates a refund.

> **Note:** The uploaded `.py` file contains a Colab-specific `!pip install` command. Remove or comment out that line before running it as a regular Python script.

## Project Background

Developed as part of **Summer of Code 2025**, with a focus on understanding Ethereum smart contracts and their practical applications in decentralized fundraising.

---

*An educational prototype tested on a local Ethereum blockchain, not intended for production use with real funds.*
