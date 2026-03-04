"""
Executive Summary: Compares custody statements versus ledger balances to flag breaks and determine severity.

Inputs: custody_positions (list[dict]), ledger_positions (list[dict]), tolerance_bps (float, optional), notify_thunder (bool, optional)
Outputs: status (str), data (breaks/summary), timestamp (str)
MCP Tool Name: custody_break_detector
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
    "name": "custody_break_detector",
    "description": "Identify cash or security breaks between custody statements and the ledger.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "custody_positions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Custody balances with account, currency, asset, balance.",
            },
            "ledger_positions": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Ledger balances for the same identifiers.",
            },
            "tolerance_bps": {
                "type": "number",
                "default": 10.0,
                "description": "Variance tolerance in basis points.",
            },
            "notify_thunder": {
                "type": "boolean",
                "default": False,
                "description": "Escalate when breaks exceed tolerance.",
            },
        },
        "required": ["custody_positions", "ledger_positions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "breaks": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def custody_break_detector(
    custody_positions: list[dict[str, Any]],
    ledger_positions: list[dict[str, Any]],
    tolerance_bps: float = 10.0,
    notify_thunder: bool = False,
) -> dict[str, Any]:
    """Compare custody statements with Ghost Ledger balances."""
    emitter = SkillTelemetryEmitter(
        "custody_break_detector",
        {
            "custody_positions": len(custody_positions or []),
            "ledger_positions": len(ledger_positions or []),
            "tolerance_bps": tolerance_bps,
        },
    )
    try:
        if tolerance_bps < 0:
            raise ValueError("tolerance_bps must be non-negative")

        custody_map = _to_position_map(custody_positions or [])
        ledger_map = _to_position_map(ledger_positions or [])

        breaks: list[dict[str, Any]] = []
        total_break_value = 0.0

        for key in sorted(set(custody_map) | set(ledger_map)):
            custody_balance = custody_map.get(key, 0.0)
            ledger_balance = ledger_map.get(key, 0.0)
            variance = ledger_balance - custody_balance
            base = custody_balance or ledger_balance
            variance_bps = _to_bps(variance, base)
            if abs(variance_bps) <= tolerance_bps:
                continue
            account, asset = key.split("|", maxsplit=1)
            breaks.append(
                {
                    "account": account,
                    "asset": asset,
                    "custody_balance": round(custody_balance, 2),
                    "ledger_balance": round(ledger_balance, 2),
                    "variance": round(variance, 2),
                    "variance_bps": round(variance_bps, 2),
                    "status": "deficit" if variance < 0 else "excess",
                }
            )
            total_break_value += abs(variance)

        summary = {
            "break_count": len(breaks),
            "total_break_value": round(total_break_value, 2),
            "tolerance_bps": tolerance_bps,
        }
        data = {"breaks": breaks, "summary": summary}
        emitter.record("ok", summary)

        if notify_thunder and breaks:
            severity = "CRITICAL" if total_break_value > 1_000_000 else "WARNING"
            _notify_thunder(
                severity=severity,
                message=f"Custody breaks detected: {len(breaks)} items totaling {total_break_value:,.0f}.",
            )

        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:  # noqa: BLE001
        logger.error(f"custody_break_detector failed: {exc}")
        _log_lesson("custody_break_detector", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _to_position_map(positions: list[dict[str, Any]]) -> dict[str, float]:
    """Return account|asset -> balance map."""
    mapping: dict[str, float] = {}
    for record in positions:
        if not isinstance(record, dict):
            continue
        account = str(record.get("account") or record.get("wallet") or "").lower()
        asset = str(record.get("asset") or record.get("currency") or "").upper()
        if not account or not asset:
            continue
        balance = float(record.get("balance") or 0.0)
        mapping[f"{account}|{asset}"] = mapping.get(f"{account}|{asset}", 0.0) + balance
    return mapping


def _to_bps(variance: float, base: float) -> float:
    """Convert variance into basis points."""
    if base == 0:
        return 0.0
    return (variance / base) * 10_000


def _notify_thunder(severity: str, message: str) -> None:
    """Send alert to Thunder with safe fallback."""
    try:
        from skills.thunder_signal import thunder_signal

        thunder_signal(severity=severity, message=message)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"custody_break_detector alert failed: {exc}")


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared lesson logger."""
    _shared_log_lesson(skill_name, error)
