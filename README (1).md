# SENTINEL — AI Real-Time Fraud Detection for Blockchain Transactions

> An AI-powered system that intercepts blockchain transactions BEFORE they are finalized on-chain, analyzes them for fraud in real-time, and either approves, flags, or permanently blocks them.

![SENTINEL Banner](https://img.shields.io/badge/SENTINEL-v1.0-5d9fff?style=for-the-badge&labelColor=05080f)
![AI Powered](https://img.shields.io/badge/AI-Claude%20Sonnet-5dffb6?style=for-the-badge&labelColor=05080f)
![License](https://img.shields.io/badge/License-MIT-ffd45d?style=for-the-badge&labelColor=05080f)

---

## The Problem

Once a blockchain transaction is finalized, **it is irreversible**. There is no "undo" button. In 2023 alone, over **$1.8 billion** was lost to crypto fraud. Current systems only detect fraud AFTER the money is gone.

## The Solution — SENTINEL

SENTINEL intercepts transactions in the **3-second pending window** before they hit the blockchain, runs a full AI fraud analysis, and blocks suspicious transactions before they become permanent.

---

## Features

- **Real-Time Interception** — catches transactions before finalization
- **6-Factor Risk Scoring** — velocity, amount, account age, time, gas, address reputation
- **Claude AI Analysis** — live written fraud report for every transaction
- **Live Transaction Feed** — simulated real-time stream with auto-mode
- **8 Fraud Patterns Database** — known attack vectors with real-world examples
- **Scan History** — full audit trail of all decisions
- **Live Stats Bar** — transactions scanned, blocked, approved, value protected

---

## Live Demo

Open `index.html` in any browser — no install needed.

Deploy on GitHub Pages:
1. Push to GitHub
2. Settings → Pages → main branch → / (root)
3. Live at `https://YOUR_USERNAME.github.io/sentinel-fraud`

---

## How It Works

```
Transaction Submitted
        ↓
INTERCEPTED (before on-chain)
        ↓
Address Profiling
  → Account age, history, blacklist check
        ↓
Behavioral Analysis
  → Velocity, timing, gas anomalies
        ↓
6-Factor Risk Score (0-100%)
        ↓
Claude AI Analysis
  → Unique fraud report, streamed live
        ↓
VERDICT
  → APPROVE (<40%) | FLAG (40-70%) | BLOCK (>70%)
        ↓
Immutable Audit Log
  → Decision recorded permanently
```

---

## Risk Factors Explained

| Factor | What it checks | Weight |
|--------|---------------|--------|
| **Velocity** | Transactions per hour from sender | 25% |
| **Amount Anomaly** | Is this amount unusually large? | 20% |
| **Account Age** | How old is the sender wallet? | 20% |
| **Address Reputation** | Is address on fraud blacklist? | 15% |
| **Time Pattern** | Is it 3AM? Unusual hours? | 10% |
| **Gas Anomaly** | Unusually high gas = rushing = suspicious | 10% |

---

## Extending to Production

### Python Backend (Real ML Model)
```python
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

def calculate_fraud_score(tx_data):
    features = [
        min(tx_data['velocity'] / 50, 1.0),
        min(tx_data['amount'] / 1000, 1.0),
        1.0 if tx_data['account_age'] == 'new' else 0.1,
        1.0 if tx_data['time'] == 'odd' else 0.1,
        min(tx_data['gas'] / 500, 1.0),
        tx_data['address_reputation_score'],
    ]
    weights = [0.25, 0.20, 0.20, 0.10, 0.10, 0.15]
    score = sum(f * w for f, w in zip(features, weights))
    return round(score * 100)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    score = calculate_fraud_score(data)
    verdict = 'BLOCK' if score > 70 else 'FLAG' if score > 40 else 'APPROVE'
    return jsonify({'score': score, 'verdict': verdict})
```

### Solidity Smart Contract (On-Chain Gate)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SentinelGate {
    address public sentinel;
    mapping(address => bool) public blocked;

    event TransactionBlocked(address from, address to, uint256 amount);
    event TransactionApproved(address from, address to, uint256 amount);

    constructor() { sentinel = msg.sender; }

    modifier onlySentinel() { require(msg.sender == sentinel); _; }

    function blockAddress(address addr) external onlySentinel {
        blocked[addr] = true;
    }

    function safeTransfer(address to) external payable {
        require(!blocked[msg.sender], "Address blocked by SENTINEL");
        emit TransactionApproved(msg.sender, to, msg.value);
        payable(to).transfer(msg.value);
    }
}
```

---

## Project Structure

```
sentinel-fraud/
├── index.html          ← Full app (single file, runs in browser)
├── README.md           ← This file
├── LICENSE             ← MIT License
└── backend/
    ├── app.py          ← Python ML backend
    └── requirements.txt
```

---

## Competition Pitch

> "Every second, millions of dollars flow through blockchain networks with zero fraud protection. Once a transaction is confirmed — the money is gone forever. SENTINEL is the world's first AI real-time fraud interceptor for blockchain. In under 3 seconds, before any transaction reaches the chain, our AI scores it across 6 risk dimensions, writes a fraud report, and either clears it or blocks it permanently. We don't chase fraud after the fact — we stop it before it happens."

---

## License

MIT — free to use, extend, and deploy.

---

*Built with Claude AI · SENTINEL v1.0*
