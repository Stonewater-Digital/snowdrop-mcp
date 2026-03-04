"""Goodwill crypto terminology glossary."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TERMS = {
    "defi": (
        "Decentralized finance platforms offering loans, swaps, and yield without banks.",
        "Like an automated co-op bank where code handles deposits and loans.",
        "Protocols can be exploited; only risk what you can lose.",
        ["liquidity_pool", "staking", "dao"],
    ),
    "nft": (
        "Non-fungible token proving ownership of a unique digital item.",
        "Comparable to a signed trading card with a digital title.",
        "Be cautious of scams and illiquid collections.",
        ["smart_contract", "marketplace"],
    ),
    "staking": (
        "Locking tokens to secure proof-of-stake networks in exchange for rewards.",
        "Similar to placing a security deposit that earns interest for keeping systems honest.",
        "Slashing can burn funds if validators misbehave.",
        ["validator", "delegation"],
    ),
    "liquidity_pool": (
        "Smart-contract vault that holds token pairs so traders can swap without order books.",
        "Think of a vending machine stocked with both sodas and coins for change.",
        "Impermanent loss can shrink balances when prices move.",
        ["amm", "defi"],
    ),
    "gas": (
        "Network fee paid to miners/validators for executing transactions.",
        "Like tipping a courier so your package gets delivered.",
        "High gas means waiting or paying more.",
        ["block", "base_fee"],
    ),
    "wallet": (
        "Software or hardware that stores private keys giving access to funds.",
        "Comparable to a password manager for your money.",
        "Losing keys often means losing funds permanently.",
        ["seed_phrase", "hot_wallet", "cold_wallet"],
    ),
    "seed_phrase": (
        "List of 12-24 words that backs up a wallet's private keys.",
        "It's the master key to a digital safe.",
        "Never share it; anyone can empty your wallet.",
        ["wallet", "mnemonic"],
    ),
    "smart_contract": (
        "Self-executing code stored on a blockchain that runs when conditions meet.",
        "Acts like a vending machine: insert exact input, get predictable output.",
        "Bugs are expensive; code can’t be recalled easily.",
        ["defi", "dao", "nft"],
    ),
    "dao": (
        "Decentralized autonomous organization where token holders vote on proposals.",
        "Like a group chat with a shared treasury that only moves with votes.",
        "Governance attacks can drain treasuries.",
        ["governance_token", "treasury"],
    ),
    "bridge": (
        "Service moving tokens across blockchains by locking on one chain and minting on another.",
        "Like a currency exchange kiosk connecting two airports.",
        "Bridges are frequent hack targets.",
        ["wrapped_token", "cross_chain"],
    ),
    "impermanent_loss": (
        "Temporary value drop LPs face when token prices diverge.",
        "Comparable to giving both apples and oranges to a stand and getting fewer apples back when apples moon.",
        "Choose pools with correlated assets to reduce risk.",
        ["liquidity_pool", "amm"],
    ),
    "mev": (
        "Miner/Maximal Extractable Value from reordering transactions for profit.",
        "Like a cashier grabbing the best coupons before scanning your cart.",
        "Front-running can hurt regular users.",
        ["sandwich_attack", "priority_gas"],
    ),
    "validator": (
        "Node that secures a proof-of-stake chain by proposing and attesting blocks.",
        "Think of an auditor stamping each page of a ledger.",
        "Downtime or fraud can slash stake.",
        ["staking", "delegation"],
    ),
    "layer2": (
        "Scaling network built atop a base chain for faster, cheaper transactions.",
        "Like an express lane feeding receipts back to the main cashier.",
        "Need to bridge funds carefully between layers.",
        ["rollup", "bridge"],
    ),
    "rollup": (
        "Layer-2 solution that batches transactions and posts compressed proofs on L1.",
        "It's like mailing a summary spreadsheet instead of every receipt.",
        "Exit windows and fraud proofs vary by design.",
        ["layer2", "optimistic_rollup", "zk_rollup"],
    ),
    "optimistic_rollup": (
        "Rollup assuming transactions are valid unless challenged.",
        "Think of a trust-but-verify system with dispute periods.",
        "Withdrawals can take days while challenge windows close.",
        ["rollup", "fraud_proof"],
    ),
    "zk_rollup": (
        "Rollup proving correctness with zero-knowledge proofs.",
        "Like sending a sealed math proof instead of revealing every step.",
        "Complex cryptography can limit hardware support.",
        ["layer2", "rollup"],
    ),
    "amm": (
        "Automated market maker that prices trades via formulas instead of order books.",
        "A digital bartender swapping drinks using ratios.",
        "Large trades can suffer slippage.",
        ["liquidity_pool", "defi"],
    ),
    "slippage": (
        "Difference between expected and executed trade price due to liquidity.",
        "Like ordering 10 coffees and moving the price by clearing the shelf.",
        "Set slippage limits to avoid surprises.",
        ["amm", "liquidity"],
    ),
    "cold_wallet": (
        "Offline storage for private keys, such as hardware wallets.",
        "Comparable to a safe deposit box.",
        "Keep backups; losing the device can mean lost funds.",
        ["wallet", "seed_phrase"],
    ),
    "hot_wallet": (
        "Always-connected wallet software (browser or mobile).",
        "Like cash in a pocket—convenient but riskier.",
        "Beware malware and phishing.",
        ["wallet", "seed_phrase"],
    ),
    "wrapped_token": (
        "Representation of an asset from another chain, backed 1:1 by locked funds.",
        "Similar to a casino chip redeemable for real cash later.",
        "Counterparty risk if custodian fails.",
        ["bridge", "cross_chain"],
    ),
    "airdrop": (
        "Free token distribution to wallets meeting certain criteria.",
        "Like a loyalty rebate for early adopters.",
        "Watch for phishing claiming fake airdrops.",
        ["snapshot", "governance_token"],
    ),
    "snapshot": (
        "Record of wallet balances at a specific block to determine eligibility.",
        "Comparable to a roll call taken at midnight.",
        "Move funds too late and you may miss rewards.",
        ["airdrop", "dao"],
    ),
    "governance_token": (
        "Token granting voting rights in DAOs or protocols.",
        "Like holding shares with ballot power.",
        "Whales can dominate votes.",
        ["dao", "proposal"],
    ),
    "proposal": (
        "Formal suggestion submitted to a DAO for voting.",
        "Similar to a board agenda item.",
        "Low turnout can let small groups decide outcomes.",
        ["dao", "governance_token"],
    ),
    "rug_pull": (
        "Exit scam where developers drain liquidity and vanish.",
        "Like a store owner running off with the register.",
        "Verify audits and team reputations.",
        ["defi", "liquidity_pool"],
    ),
    "kyc": (
        "Know Your Customer identity checks exchanges perform.",
        "Comparable to opening a bank account.",
        "Sharing PII means trusting custodians.",
        ["exchange", "compliance"],
    ),
    "exchange": (
        "Platform to trade crypto assets for other tokens or fiat.",
        "Acts like a stock exchange for digital coins.",
        "Centralized exchanges hold your keys.",
        ["kyc", "wallet"],
    ),
    "halving": (
        "Bitcoin event cutting block rewards roughly every four years.",
        "Like reducing gold mine output overnight.",
        "Volatility often spikes around halvings.",
        ["bitcoin", "supply"],
    ),
    "difficulty": (
        "Measurement of how hard it is to find a valid block hash in PoW chains.",
        "Comparable to tightening a combination lock.",
        "Impacts miner profitability.",
        ["mining", "bitcoin"],
    ),
    "mining": (
        "Proof-of-work process of solving puzzles to add blocks and earn rewards.",
        "Like a giant bingo game where winners collect coins.",
        "Needs significant electricity and hardware.",
        ["difficulty", "halving"],
    ),
    "hard_fork": (
        "Protocol change that is not backward compatible, splitting the chain if nodes disagree.",
        "Comparable to a rulebook rewrite mid-season.",
        "Coins on minority chain may lose value.",
        ["soft_fork", "upgrade"],
    ),
    "soft_fork": (
        "Backward-compatible upgrade tightening rules.",
        "Like introducing stricter dress code that old outfits still meet.",
        "Still requires majority support to activate.",
        ["hard_fork", "upgrade"],
    ),
    "oracle": (
        "Service feeding external data (prices, events) into smart contracts.",
        "Acts like a data courier delivering weather reports to code.",
        "Centralized oracles can be single points of failure.",
        ["smart_contract", "defi"],
    ),
}

TOOL_META: dict[str, Any] = {
    "name": "crypto_glossary",
    "description": "Explains crypto terms with analogies and risk warnings (goodwill only).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "term": {"type": "string"},
        },
        "required": ["term"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def crypto_glossary(term: str, **_: Any) -> dict[str, Any]:
    """Return definition, analogy, risk notes, and related words."""
    try:
        term_key = term.lower()
        if term_key not in TERMS:
            raise ValueError("Term not available")
        definition, analogy, warning, related = TERMS[term_key]
        data = {
            "term": term,
            "definition": definition,
            "analogy": analogy,
            "risk_warning": warning,
            "related_terms": related,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("crypto_glossary", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
