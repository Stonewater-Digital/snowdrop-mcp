"""Estimate batch gas usage and translate it into fee forecasts.
Helps plan execution budgets for multi-call smart contract workflows."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "smart_contract_gas_estimator",
    "description": "Aggregates gas consumption inputs and converts them to native and USD fee estimates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "gas_units": {"type": "number", "description": "Estimated gas units for the operation"},
                        "count": {"type": "number", "description": "Expected number of repetitions", "default": 1},
                    },
                    "required": ["gas_units"],
                },
                "description": "Sequence of planned contract calls with gas estimates.",
            },
            "base_fee_gwei": {"type": "number", "description": "Projected base fee per gas in gwei"},
            "priority_fee_gwei": {"type": "number", "description": "Priority tip per gas in gwei"},
            "native_token_price_usd": {"type": "number", "description": "Spot price of the native token in USD"},
        },
        "required": ["operations", "base_fee_gwei", "priority_fee_gwei", "native_token_price_usd"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def smart_contract_gas_estimator(
    operations: Sequence[dict[str, float]],
    base_fee_gwei: float,
    priority_fee_gwei: float,
    native_token_price_usd: float,
    **_: Any,
) -> dict[str, Any]:
    """Summarize gas exposure and translate to total fee expectations.

    Args:
        operations: Iterable of gas estimates and call counts.
        base_fee_gwei: Projected base fee component per gas unit.
        priority_fee_gwei: Priority tip per gas unit.
        native_token_price_usd: USD price of the native token backing the network.

    Returns:
        Status payload containing native token and USD fee forecasts.
    """
    try:
        total_gas_units = sum(float(item.get("gas_units", 0)) * float(item.get("count", 1)) for item in operations)
        total_fee_gwei = total_gas_units * (base_fee_gwei + priority_fee_gwei)
        total_fee_native = total_fee_gwei / 1_000_000_000
        estimated_fee_usd = total_fee_native * native_token_price_usd
        data = {
            "total_gas_units": round(total_gas_units, 2),
            "effective_gwei_per_gas": round(base_fee_gwei + priority_fee_gwei, 4),
            "fee_native": round(total_fee_native, 6),
            "fee_usd": round(estimated_fee_usd, 2),
            "base_fee_gwei": base_fee_gwei,
            "priority_fee_gwei": priority_fee_gwei,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("smart_contract_gas_estimator failure: %s", exc)
        log_lesson(f"smart_contract_gas_estimator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
