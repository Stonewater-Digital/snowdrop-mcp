"""
Executive Summary: Daily reconciliation engine that compares live Kraken balances against the Ghost Ledger and alerts Thunder on any discrepancy.

Inputs: spreadsheet_url (str) — full URL of the active Ghost Ledger Google Sheet
Outputs: dict with matched (bool), kraken_balance (float), ledger_balance (float), discrepancies (list)
MCP Tool Name: reconcile
"""
import logging
from typing import Any
from datetime import datetime, timezone

from skills.audit_kraken import audit_kraken
from skills.ghost_ledger import ghost_ledger

logger = logging.getLogger("snowdrop.skills")

# Tolerance in USD — zero tolerance by design (Fund Accounting bedrock principle)
RECONCILIATION_TOLERANCE: float = 0.00

# --- MCP Tool Metadata ---
TOOL_META = {
    "name": "reconcile",
    "description": (
        "Daily reconciliation engine. Compares live Kraken exchange balances against "
        "the Ghost Ledger (Google Sheets). Emits a CRITICAL alert to Thunder via Telegram "
        "if any discrepancy is detected. Zero-tolerance policy."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "spreadsheet_url": {
                "type": "string",
                "description": "Full URL of the active Ghost Ledger Google Spreadsheet.",
            }
        },
        "required": ["spreadsheet_url"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "matched": {"type": "boolean"},
                    "kraken_balance": {"type": "number"},
                    "ledger_balance": {"type": "number"},
                    "discrepancies": {
                        "type": "array",
                        "items": {"type": "object"},
                    },
                    "timestamp": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}


def reconcile(spreadsheet_url: str, **kwargs: Any) -> dict:
    """Run a daily reconciliation between Kraken live balances and the Ghost Ledger.

    Executes a three-step reconciliation process:
        1. Fetch live asset balances from Kraken via audit_kraken().
        2. Read the current ledger balance from THE VAULT tab via ghost_ledger().
        3. Compare the two totals with zero-dollar tolerance.

    If a discrepancy is found, a CRITICAL alert is dispatched to Thunder via
    thunder_signal. The result is always returned regardless of alert status.

    Args:
        spreadsheet_url: Full URL of the Ghost Ledger Google Spreadsheet.
        **kwargs: Unused. Accepted for MCP dispatch compatibility.

    Returns:
        dict: A result dict with the following shape on success::

            {
                "status": "success",
                "data": {
                    "matched": True,
                    "kraken_balance": 1500.00,
                    "ledger_balance": 1500.00,
                    "discrepancies": [],
                    "timestamp": "2026-02-19T00:00:00+00:00"
                },
                "timestamp": "2026-02-19T00:00:00+00:00"
            }

        On discrepancy, "matched" is False and "discrepancies" contains detail dicts.
        On error::

            {
                "status": "error",
                "error": "<error message>",
                "timestamp": "2026-02-19T00:00:00+00:00"
            }
    """
    try:
        # --- Step 1: Fetch live Kraken balances ---
        kraken_result = audit_kraken()
        if kraken_result.get("status") != "success":
            raise RuntimeError(f"audit_kraken returned error: {kraken_result.get('error')}")

        kraken_balance: float = float(kraken_result["data"]["total_usd"])
        kraken_asset_breakdown: list[dict] = kraken_result["data"].get("balances", [])

        # --- Step 2: Fetch Ghost Ledger balance ---
        ledger_result = ghost_ledger(action="get_balance", spreadsheet_url=spreadsheet_url)
        if ledger_result.get("status") != "success":
            raise RuntimeError(f"ghost_ledger.get_balance returned error: {ledger_result.get('error')}")

        ledger_balance: float = float(ledger_result["data"]["ledger_balance"])

        # --- Step 3: Compare with zero-tolerance policy ---
        delta: float = abs(kraken_balance - ledger_balance)
        matched: bool = delta <= RECONCILIATION_TOLERANCE

        discrepancies: list[dict] = []
        if not matched:
            discrepancy = {
                "type": "BALANCE_MISMATCH",
                "kraken_total_usd": kraken_balance,
                "ledger_total_usd": ledger_balance,
                "delta_usd": round(delta, 2),
                "tolerance_usd": RECONCILIATION_TOLERANCE,
                "kraken_asset_breakdown": kraken_asset_breakdown,
            }
            discrepancies.append(discrepancy)

            logger.warning(
                f"reconcile: DISCREPANCY DETECTED — kraken={kraken_balance:.2f}, "
                f"ledger={ledger_balance:.2f}, delta={delta:.2f}"
            )

            # --- Alert Thunder on discrepancy ---
            _alert_thunder(kraken_balance=kraken_balance, ledger_balance=ledger_balance, delta=delta)
        else:
            logger.info(
                f"reconcile: MATCHED — kraken={kraken_balance:.2f}, ledger={ledger_balance:.2f}"
            )

        result_data: dict[str, Any] = {
            "matched": matched,
            "kraken_balance": kraken_balance,
            "ledger_balance": ledger_balance,
            "discrepancies": discrepancies,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        return {
            "status": "success",
            "data": result_data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"reconcile failed: {e}")
        _log_lesson(f"reconcile: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _alert_thunder(kraken_balance: float, ledger_balance: float, delta: float) -> None:
    """Fire a CRITICAL Telegram alert to Thunder when a reconciliation discrepancy is found.

    Imported lazily to avoid circular dependencies and to keep thunder_signal
    as a standalone module.

    Args:
        kraken_balance: Live Kraken total balance in USD.
        ledger_balance: Ghost Ledger recorded balance in USD.
        delta: Absolute difference between the two balances in USD.
    """
    try:
        from skills.thunder_signal import thunder_signal

        message = (
            f"RECONCILIATION DISCREPANCY DETECTED\n\n"
            f"Kraken Balance: ${kraken_balance:,.2f} USD\n"
            f"Ledger Balance: ${ledger_balance:,.2f} USD\n"
            f"Delta: ${delta:,.2f} USD\n\n"
            f"Tolerance is $0.00. Immediate review required."
        )
        thunder_signal(severity="CRITICAL", message=message)

    except Exception as e:
        logger.error(f"reconcile._alert_thunder failed to send signal: {e}")
        _log_lesson(f"reconcile._alert_thunder: {e}")


def _log_lesson(message: str) -> None:
    """Append a timestamped error lesson to logs/lessons.md.

    Args:
        message: Human-readable description of what went wrong.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
