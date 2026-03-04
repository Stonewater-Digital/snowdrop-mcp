"""
Executive Summary: Compares ledger-tracked wallet balances against on-chain data and flags variances above tolerance.

Inputs: ledger_positions (list[dict]), chain_balances (list[dict]), tolerance_pct (float, optional)
Outputs: status (str), data (reconciliations/summary), timestamp (str)
MCP Tool Name: blockchain_wallet_reconciler
"""
from __future__ import annotations

from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

TOOL_META: dict[str, Any] = {
    "name": "blockchain_wallet_reconciler",
    "description": "Reconciles Ghost Ledger wallet balances against on-chain snapshots and surfaces tolerance breaches.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ledger_positions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Ledger entries with wallet, asset, and balance fields.",
            },
            "chain_balances": {
                "type": "array",
                "items": {"type": "object"},
                "description": "On-chain balances containing wallet, asset, balance.",
            },
            "tolerance_pct": {
                "type": "number",
                "default": 0.5,
                "description": "Allowed percentage variance before raising a break.",
            },
        },
        "required": ["ledger_positions", "chain_balances"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "reconciliations": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def blockchain_wallet_reconciler(
    ledger_positions: list[dict[str, Any]],
    chain_balances: list[dict[str, Any]],
    tolerance_pct: float = 0.5,
) -> dict[str, Any]:
    """Compare ledger balances against on-chain readings.

    Args:
        ledger_positions: Ghost Ledger holdings keyed by wallet+asset.
        chain_balances: On-chain pulled balances using the same identifiers.
        tolerance_pct: Allowed percent variance before break escalation.

    Returns:
        Snowdrop response dict listing reconciliations and summary metrics.

    Raises:
        ValueError: If payloads are not iterable or tolerance is negative.
    """
    emitter = SkillTelemetryEmitter(
        "blockchain_wallet_reconciler",
        {
            "ledger_positions": len(ledger_positions or []),
            "chain_balances": len(chain_balances or []),
            "tolerance_pct": tolerance_pct,
        },
    )
    try:
        if tolerance_pct < 0:
            raise ValueError("tolerance_pct must be >= 0")
        ledger_map = _build_position_map(ledger_positions or [])
        chain_map = _build_position_map(chain_balances or [])

        reconciliations: list[dict[str, Any]] = []
        status_counts = {"ok": 0, "variance": 0, "missing_on_chain": 0, "missing_in_ledger": 0}

        for key in sorted(set(ledger_map) | set(chain_map)):
            ledger_balance = ledger_map.get(key, 0.0)
            chain_balance = chain_map.get(key, 0.0)
            variance_units = round(chain_balance - ledger_balance, 8)
            pct = _variance_pct(ledger_balance, chain_balance)
            wallet, asset = key.split("|", maxsplit=1)

            if key not in ledger_map:
                status_counts["missing_in_ledger"] += 1
                status = "missing_in_ledger"
            elif key not in chain_map:
                status_counts["missing_on_chain"] += 1
                status = "missing_on_chain"
            elif abs(pct) > tolerance_pct:
                status_counts["variance"] += 1
                status = "variance"
            else:
                status_counts["ok"] += 1
                status = "ok"

            reconciliations.append(
                {
                    "wallet": wallet,
                    "asset": asset,
                    "ledger_balance": ledger_balance,
                    "chain_balance": chain_balance,
                    "variance_units": variance_units,
                    "variance_pct": pct,
                    "status": status,
                }
            )

        summary = {
            "positions": len(reconciliations),
            **status_counts,
            "tolerance_pct": tolerance_pct,
        }
        emitter.record(
            "ok",
            {
                "positions": len(reconciliations),
                "breaks": status_counts["variance"]
                + status_counts["missing_on_chain"]
                + status_counts["missing_in_ledger"],
            },
        )
        return {
            "status": "ok",
            "data": {"reconciliations": reconciliations, "summary": summary},
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:
        msg = f"blockchain_wallet_reconciler failed: {exc}"
        logger.error(msg)
        _log_lesson("blockchain_wallet_reconciler", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _build_position_map(positions: list[dict[str, Any]]) -> dict[str, float]:
    """Return wallet|asset -> balance map."""
    position_map: dict[str, float] = {}
    for item in positions:
        if not isinstance(item, dict):
            continue
        wallet = str(item.get("wallet") or "").strip().lower()
        asset = str(item.get("asset") or "").strip().upper()
        if not wallet or not asset:
            continue
        balance = _to_float(item.get("balance")) or 0.0
        key = f"{wallet}|{asset}"
        position_map[key] = balance
    return position_map


def _variance_pct(ledger_balance: float, chain_balance: float) -> float:
    """Return percent variance using ledger as denominator when available."""
    denominator = ledger_balance if ledger_balance not in (0, None) else chain_balance
    if not denominator:
        return 0.0
    return round((chain_balance - ledger_balance) / denominator * 100, 6)


def _to_float(value: Any) -> float | None:
    """Convert values to floats safely."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy to shared lesson logger for consistent formatting."""
    _shared_log_lesson(skill_name, error)
