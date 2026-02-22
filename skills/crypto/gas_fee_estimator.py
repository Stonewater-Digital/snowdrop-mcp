"""Estimate TON/SOL gas fees with conservative fallbacks."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TON_BASE_TON = 0.03
TON_PER_BYTE = 0.000001
SOL_BASE_SOL = 0.00001
SOL_PER_BYTE = 0.000000001
PRIORITY_MULTIPLIERS = {
    "economy": 0.8,
    "standard": 1.0,
    "urgent": 1.5,
}

TOOL_META: dict[str, Any] = {
    "name": "gas_fee_estimator",
    "description": "Provides conservative fee estimates for TON and SOL transfers.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "chain": {"type": "string", "enum": ["ton", "sol"]},
            "tx_size_bytes": {"type": "number"},
            "priority": {"type": "string"},
        },
        "required": ["chain", "tx_size_bytes"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "estimated_fee": {"type": "number"},
                    "unit": {"type": "string"},
                    "components": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def gas_fee_estimator(
    chain: str,
    tx_size_bytes: float,
    priority: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Estimate transaction fees."""
    try:
        if tx_size_bytes <= 0:
            raise ValueError("tx_size_bytes must be positive")
        normalized_chain = chain.lower()
        if normalized_chain not in {"ton", "sol"}:
            raise ValueError("chain must be 'ton' or 'sol'")
        priority_key = (priority or "standard").lower()
        multiplier = PRIORITY_MULTIPLIERS.get(priority_key)
        if multiplier is None:
            raise ValueError("priority must be economy/standard/urgent")

        if normalized_chain == "ton":
            unit = "TON"
            base = TON_BASE_TON
            variable = TON_PER_BYTE * tx_size_bytes
        else:
            unit = "SOL"
            base = SOL_BASE_SOL
            variable = SOL_PER_BYTE * tx_size_bytes

        estimated = (base + variable) * multiplier
        data = {
            "chain": normalized_chain,
            "estimated_fee": round(estimated, 8),
            "unit": unit,
            "components": {
                "base": round(base, 8),
                "variable": round(variable, 8),
                "priority_multiplier": multiplier,
            },
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("gas_fee_estimator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
