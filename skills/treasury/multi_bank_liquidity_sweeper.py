"""
Executive Summary: Evaluates multi-bank cash positions and recommends sweep instructions to maintain policy buffers.

Inputs: accounts (list[dict]), notify_thunder (bool, optional)
Outputs: status (str), data (instructions/summary), timestamp (str)
MCP Tool Name: multi_bank_liquidity_sweeper
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
)

POLICY_PATH = Path("config/treasury_policies.yaml")

TOOL_META: dict[str, Any] = {
    "name": "multi_bank_liquidity_sweeper",
    "description": "Recommend cash sweeps across multiple banks using target min/max policies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "accounts": {
                "type": "array",
                "items": {"type": "object"},
                "description": (
                    "List with keys: bank, account_id, balance, target_min, target_max, sweep_destination."
                ),
            },
            "notify_thunder": {
                "type": "boolean",
                "default": False,
                "description": "Escalate when aggregate deficit exceeds the policy threshold.",
            },
        },
        "required": ["accounts"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "instructions": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def multi_bank_liquidity_sweeper(
    accounts: list[dict[str, Any]],
    notify_thunder: bool = False,
) -> dict[str, Any]:
    """Generate sweep instructions for multi-bank cash."""
    emitter = SkillTelemetryEmitter(
        "multi_bank_liquidity_sweeper",
        {"accounts": len(accounts or [])},
    )
    try:
        if not accounts:
            raise ValueError("accounts cannot be empty")

        policies = _load_policies()
        instructions: list[dict[str, Any]] = []
        deficit_total = 0.0
        surplus_total = 0.0

        for record in accounts:
            bank = str(record.get("bank") or "unknown")
            account_id = str(record.get("account_id") or bank)
            balance = float(record.get("balance") or 0.0)
            target_min = float(record.get("target_min") or 0.0)
            target_max = float(record.get("target_max") or target_min)
            destination = record.get("sweep_destination") or policies["sweep_destinations"].get("tier1")

            if balance > target_max:
                excess = balance - target_max
                surplus_total += excess
                instructions.append(
                    {
                        "action": "sweep_out",
                        "bank": bank,
                        "account_id": account_id,
                        "amount": round(excess, 2),
                        "destination": destination,
                        "reason": "above_target_max",
                    }
                )
            elif balance < target_min:
                deficit = target_min - balance
                deficit_total += deficit
                instructions.append(
                    {
                        "action": "fund_account",
                        "bank": bank,
                        "account_id": account_id,
                        "amount": round(deficit, 2),
                        "source": policies["sweep_destinations"].get("tier2"),
                        "reason": "below_policy_floor",
                    }
                )

        summary = {
            "accounts": len(accounts),
            "deficit_total": round(deficit_total, 2),
            "surplus_total": round(surplus_total, 2),
        }
        data = {"instructions": instructions, "summary": summary}
        emitter.record(
            "ok",
            {"instruction_count": len(instructions), "deficit_total": deficit_total},
        )

        if notify_thunder and deficit_total >= policies["escalation_threshold_usd"]:
            _notify_thunder(
                severity="WARNING",
                message=f"Bank liquidity deficit {deficit_total:,.0f} exceeds policy. {len(instructions)} actions required.",
            )

        return {"status": "ok", "data": data, "timestamp": get_iso_timestamp()}
    except Exception as exc:  # noqa: BLE001
        logger.error(f"multi_bank_liquidity_sweeper failed: {exc}")
        _log_lesson("multi_bank_liquidity_sweeper", str(exc))
        emitter.record("error", {"error": str(exc)})
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": get_iso_timestamp()}


def _load_policies() -> dict[str, Any]:
    """Return treasury policies for sweep routing."""
    defaults = {
        "escalation_threshold_usd": 500_000.0,
        "sweep_destinations": {"tier1": "money_market", "tier2": "t_bills"},
    }
    try:
        if POLICY_PATH.exists():
            with POLICY_PATH.open(encoding="utf-8") as handle:
                payload = yaml.safe_load(handle) or {}
                defaults.update(payload)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"multi_bank_liquidity_sweeper: failed to load policies: {exc}")
    if "sweep_destinations" not in defaults:
        defaults["sweep_destinations"] = {"tier1": "money_market", "tier2": "t_bills"}
    return defaults


def _notify_thunder(severity: str, message: str) -> None:
    """Fire Thunder alert when liquidity deficits breach thresholds."""
    try:
        from skills.thunder_signal import thunder_signal

        thunder_signal(severity=severity, message=message)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"multi_bank_liquidity_sweeper alert failed: {exc}")


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared logger."""
    _shared_log_lesson(skill_name, error)
