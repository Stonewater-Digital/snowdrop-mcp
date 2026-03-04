"""
Executive Summary: Reconciles a CBDC transaction ledger against central bank balance and reported circulation to detect issuance discrepancies.
Inputs: cbdc_ledger (list[dict]: tx_id, amount, sender, receiver, timestamp), central_bank_balance (float), reported_circulation (float)
Outputs: ledger_balance (float), circulation_match (bool), discrepancies (list), net_issuance (float)
MCP Tool Name: central_bank_ledger_sync
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "central_bank_ledger_sync",
    "description": "Reconciles a CBDC transaction ledger against central bank balance and reported circulation figures to detect discrepancies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cbdc_ledger": {
                "type": "array",
                "description": "List of CBDC transactions",
                "items": {
                    "type": "object",
                    "properties": {
                        "tx_id": {"type": "string"},
                        "amount": {"type": "number", "description": "Positive = mint/issuance, negative = burn/redemption"},
                        "sender": {"type": "string"},
                        "receiver": {"type": "string"},
                        "timestamp": {"type": "string"}
                    },
                    "required": ["tx_id", "amount", "sender", "receiver", "timestamp"]
                }
            },
            "central_bank_balance": {"type": "number", "description": "Authoritative balance at central bank in currency units"},
            "reported_circulation": {"type": "number", "description": "Official reported CBDC in circulation"}
        },
        "required": ["cbdc_ledger", "central_bank_balance", "reported_circulation"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "ledger_balance": {"type": "number"},
                    "circulation_match": {"type": "boolean"},
                    "discrepancies": {"type": "array"},
                    "net_issuance": {"type": "number"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}

# Central bank sender/receiver identifiers indicating mint or burn events
CENTRAL_BANK_IDS = {"central_bank", "cb", "mint", "treasury", "issuer"}
BURN_RECEIVERS = {"burn", "destroy", "redemption", "retired", "void"}
TOLERANCE = 0.01  # Acceptable reconciliation tolerance in currency units


def central_bank_ledger_sync(
    cbdc_ledger: list[dict[str, Any]],
    central_bank_balance: float,
    reported_circulation: float,
    **kwargs: Any
) -> dict[str, Any]:
    """Reconcile a CBDC ledger against central bank balance and reported circulation.

    Identifies minting (issuance) and burning (redemption) transactions by
    inspecting sender/receiver fields. Verifies that:
      (1) net_issuance = minted - burned == reported_circulation
      (2) sum of all ledger amounts matches central_bank_balance within TOLERANCE

    Args:
        cbdc_ledger: Chronological list of CBDC transactions. Each dict must
            contain 'tx_id' (str), 'amount' (float, positive=mint, negative=burn),
            'sender' (str), 'receiver' (str), 'timestamp' (str ISO-8601).
        central_bank_balance: The authoritative central bank ledger balance
            in currency units (the "source of truth").
        reported_circulation: The officially reported amount of CBDC in
            active circulation.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): Reconciliation results including ledger_balance,
              net_issuance, circulation_match, discrepancies list,
              transaction statistics, and integrity flags.
            - timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        if not isinstance(cbdc_ledger, list):
            raise TypeError("cbdc_ledger must be a list of transaction dicts")

        central_bank_balance = float(central_bank_balance)
        reported_circulation = float(reported_circulation)

        discrepancies: list[dict[str, Any]] = []
        tx_ids_seen: set[str] = set()
        duplicate_txs: list[str] = []

        total_minted: float = 0.0
        total_burned: float = 0.0
        ledger_sum: float = 0.0

        processed_txs: list[dict[str, Any]] = []

        for tx in cbdc_ledger:
            tx_id = str(tx.get("tx_id", "UNKNOWN"))
            amount = float(tx.get("amount", 0.0))
            sender = str(tx.get("sender", "")).lower().strip()
            receiver = str(tx.get("receiver", "")).lower().strip()
            timestamp = str(tx.get("timestamp", ""))

            # Duplicate detection
            if tx_id in tx_ids_seen:
                duplicate_txs.append(tx_id)
                discrepancies.append({
                    "type": "DUPLICATE_TX",
                    "tx_id": tx_id,
                    "detail": "Transaction ID appears more than once in ledger"
                })
            tx_ids_seen.add(tx_id)

            # Classify transaction type
            is_mint = sender in CENTRAL_BANK_IDS and receiver not in BURN_RECEIVERS
            is_burn = receiver in BURN_RECEIVERS or (
                sender not in CENTRAL_BANK_IDS and receiver in CENTRAL_BANK_IDS
            )

            if is_mint:
                total_minted += abs(amount)
                tx_type = "MINT"
            elif is_burn:
                total_burned += abs(amount)
                tx_type = "BURN"
            else:
                tx_type = "TRANSFER"

            ledger_sum += amount

            processed_txs.append({
                "tx_id": tx_id,
                "amount": amount,
                "sender": sender,
                "receiver": receiver,
                "timestamp": timestamp,
                "type": tx_type,
            })

        net_issuance: float = round(total_minted - total_burned, 6)
        ledger_balance: float = round(ledger_sum, 6)

        # Check 1: ledger sum vs. central_bank_balance
        balance_delta = abs(ledger_balance - central_bank_balance)
        balance_match = balance_delta <= TOLERANCE
        if not balance_match:
            discrepancies.append({
                "type": "BALANCE_MISMATCH",
                "ledger_balance": ledger_balance,
                "central_bank_balance": central_bank_balance,
                "delta": round(ledger_balance - central_bank_balance, 6),
                "detail": f"Ledger sum differs from central bank balance by {balance_delta:.6f} units"
            })

        # Check 2: net_issuance vs. reported_circulation
        circulation_delta = abs(net_issuance - reported_circulation)
        circulation_match = circulation_delta <= TOLERANCE
        if not circulation_match:
            discrepancies.append({
                "type": "CIRCULATION_MISMATCH",
                "net_issuance": net_issuance,
                "reported_circulation": reported_circulation,
                "delta": round(net_issuance - reported_circulation, 6),
                "detail": "Minted minus burned does not match reported circulation"
            })

        # Check 3: negative amount transactions that are not burns
        for tx in processed_txs:
            if tx["amount"] < 0 and tx["type"] == "TRANSFER":
                discrepancies.append({
                    "type": "NEGATIVE_TRANSFER",
                    "tx_id": tx["tx_id"],
                    "amount": tx["amount"],
                    "detail": "Negative transfer amount from non-central-bank sender — potential fraud vector"
                })

        result: dict[str, Any] = {
            "ledger_balance": ledger_balance,
            "net_issuance": net_issuance,
            "total_minted": round(total_minted, 6),
            "total_burned": round(total_burned, 6),
            "reported_circulation": reported_circulation,
            "central_bank_balance": central_bank_balance,
            "circulation_match": circulation_match,
            "balance_match": balance_match,
            "fully_reconciled": circulation_match and balance_match and not duplicate_txs,
            "discrepancies": discrepancies,
            "discrepancy_count": len(discrepancies),
            "tx_count": len(cbdc_ledger),
            "duplicate_tx_ids": duplicate_txs,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"central_bank_ledger_sync failed: {e}")
        _log_lesson(f"central_bank_ledger_sync: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson/error entry to the shared lessons log.

    Args:
        message: Human-readable error or lesson description to append.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except Exception as log_err:
        logger.warning(f"_log_lesson write failed: {log_err}")
