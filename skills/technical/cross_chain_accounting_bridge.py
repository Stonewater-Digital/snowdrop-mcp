"""
Executive Summary: Normalize TON, Solana, and Ethereum transactions into a single unified ledger with net positions per chain.
Inputs: transactions (list of dicts: chain, tx_hash, amount, token, usd_value, timestamp, direction)
Outputs: unified_ledger (list), by_chain (dict), total_usd_value (float), transaction_count (int)
MCP Tool Name: cross_chain_accounting_bridge
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cross_chain_accounting_bridge",
    "description": "Normalize TON, Solana, and Ethereum transactions into a unified single ledger with net positions per chain.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transactions": {
                "type": "array",
                "description": "List of transaction dicts, each with: chain, tx_hash, amount, token, usd_value, timestamp, direction (in/out).",
                "items": {
                    "type": "object",
                    "properties": {
                        "chain": {"type": "string"},
                        "tx_hash": {"type": "string"},
                        "amount": {"type": "number"},
                        "token": {"type": "string"},
                        "usd_value": {"type": "number"},
                        "timestamp": {"type": "string"},
                        "direction": {"type": "string", "enum": ["in", "out"]}
                    },
                    "required": ["chain", "tx_hash", "amount", "token", "usd_value", "timestamp", "direction"]
                }
            }
        },
        "required": ["transactions"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "unified_ledger": {"type": "array"},
            "by_chain": {"type": "object"},
            "total_usd_value": {"type": "number"},
            "transaction_count": {"type": "integer"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["unified_ledger", "by_chain", "total_usd_value", "transaction_count", "status", "timestamp"]
    }
}

# Canonical chain name normalization map
_CHAIN_ALIASES: dict[str, str] = {
    "ton": "TON",
    "the open network": "TON",
    "sol": "SOL",
    "solana": "SOL",
    "eth": "ETH",
    "ethereum": "ETH",
    "evm": "ETH",
}

# Known stablecoin tokens for tagging
_STABLECOINS = {"USDC", "USDT", "DAI", "BUSD", "PYUSD", "USDE"}


def _normalize_chain(chain_raw: str) -> str:
    """Normalize a chain name to its canonical uppercase form.

    Args:
        chain_raw: Raw chain identifier string from the transaction.

    Returns:
        Canonical chain name (e.g. "TON", "SOL", "ETH") or uppercased original.
    """
    return _CHAIN_ALIASES.get(chain_raw.strip().lower(), chain_raw.strip().upper())


def _parse_timestamp(ts: str) -> str:
    """Parse and normalize a timestamp string to ISO 8601 UTC.

    Args:
        ts: Timestamp string in any common format.

    Returns:
        ISO 8601 UTC timestamp string.
    """
    try:
        # Try parsing as float unix timestamp
        return datetime.fromtimestamp(float(ts), tz=timezone.utc).isoformat()
    except (ValueError, TypeError):
        pass
    try:
        # Try ISO format parse
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).isoformat()
    except (ValueError, AttributeError):
        return ts  # Return raw if unparseable


def cross_chain_accounting_bridge(transactions: list[dict]) -> dict:
    """Normalize multi-chain transactions into a unified ledger with net positions.

    Each transaction is validated, enriched, and normalized. Net positions are
    computed per chain as (sum of inflows - sum of outflows) in USD. The unified
    ledger row includes a signed_usd_value field where inflows are positive and
    outflows are negative for standard double-entry-compatible reporting.

    Args:
        transactions: List of transaction dicts. Each must contain:
            - chain (str): Blockchain identifier (e.g. "TON", "SOL", "ETH").
            - tx_hash (str): Transaction hash or ID.
            - amount (float): Token amount transferred.
            - token (str): Token symbol (e.g. "TON", "SOL", "USDC").
            - usd_value (float): USD equivalent at time of transaction.
            - timestamp (str): ISO 8601 or unix timestamp.
            - direction (str): "in" (received) or "out" (sent).

    Returns:
        A dict with keys:
            - unified_ledger (list): Normalized transaction records.
            - by_chain (dict): Net USD position per chain (positive = net inflow).
            - total_usd_value (float): Sum of all net positions across all chains.
            - transaction_count (int): Total number of transactions processed.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        if not isinstance(transactions, list):
            raise TypeError(f"transactions must be a list, got {type(transactions).__name__}.")

        unified_ledger: list[dict] = []
        by_chain: dict[str, dict] = {}

        required_fields = {"chain", "tx_hash", "amount", "token", "usd_value", "timestamp", "direction"}

        for idx, tx in enumerate(transactions):
            missing = required_fields - set(tx.keys())
            if missing:
                raise ValueError(f"Transaction at index {idx} missing fields: {missing}.")

            direction = tx["direction"].strip().lower()
            if direction not in ("in", "out"):
                raise ValueError(
                    f"Transaction at index {idx} has invalid direction '{tx['direction']}', must be 'in' or 'out'."
                )

            chain = _normalize_chain(str(tx["chain"]))
            token = str(tx["token"]).strip().upper()
            usd_value = float(tx["usd_value"])
            amount = float(tx["amount"])

            # Signed USD: inflows positive, outflows negative (double-entry compatible)
            signed_usd = usd_value if direction == "in" else -usd_value
            signed_amount = amount if direction == "in" else -amount

            normalized = {
                "chain": chain,
                "tx_hash": str(tx["tx_hash"]).strip(),
                "token": token,
                "amount": amount,
                "signed_amount": signed_amount,
                "usd_value": usd_value,
                "signed_usd_value": signed_usd,
                "direction": direction,
                "timestamp_raw": str(tx["timestamp"]),
                "timestamp_utc": _parse_timestamp(str(tx["timestamp"])),
                "is_stablecoin": token in _STABLECOINS,
                "chain_native": token in {"TON", "SOL", "ETH", "BTC", "BNB"},
                "ledger_index": idx,
            }
            unified_ledger.append(normalized)

            # Accumulate by_chain net positions
            if chain not in by_chain:
                by_chain[chain] = {
                    "net_usd": 0.0,
                    "total_inflow_usd": 0.0,
                    "total_outflow_usd": 0.0,
                    "transaction_count": 0,
                    "tokens": {},
                }

            by_chain[chain]["net_usd"] = round(by_chain[chain]["net_usd"] + signed_usd, 8)
            by_chain[chain]["transaction_count"] += 1

            if direction == "in":
                by_chain[chain]["total_inflow_usd"] = round(
                    by_chain[chain]["total_inflow_usd"] + usd_value, 8
                )
            else:
                by_chain[chain]["total_outflow_usd"] = round(
                    by_chain[chain]["total_outflow_usd"] + usd_value, 8
                )

            # Per-token breakdown within each chain
            if token not in by_chain[chain]["tokens"]:
                by_chain[chain]["tokens"][token] = {"net_amount": 0.0, "net_usd": 0.0}
            by_chain[chain]["tokens"][token]["net_amount"] = round(
                by_chain[chain]["tokens"][token]["net_amount"] + signed_amount, 8
            )
            by_chain[chain]["tokens"][token]["net_usd"] = round(
                by_chain[chain]["tokens"][token]["net_usd"] + signed_usd, 8
            )

        # Total across all chains
        total_usd_value = round(sum(c["net_usd"] for c in by_chain.values()), 8)

        # Sort unified ledger by timestamp ascending
        unified_ledger.sort(key=lambda r: r["timestamp_utc"])

        return {
            "status": "success",
            "unified_ledger": unified_ledger,
            "by_chain": by_chain,
            "total_usd_value": total_usd_value,
            "transaction_count": len(unified_ledger),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"cross_chain_accounting_bridge failed: {e}")
        _log_lesson(f"cross_chain_accounting_bridge: {e}")
        return {
            "status": "error",
            "error": str(e),
            "unified_ledger": [],
            "by_chain": {},
            "total_usd_value": 0.0,
            "transaction_count": 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
