"""Calculate REIT debt to gross asset value metrics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "loan_to_value_reit",
    "description": "Calculates gross and net loan-to-value ratios for REIT balance sheets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_debt": {"type": "number"},
            "gross_asset_value": {"type": "number"},
            "cash_and_restricted": {"type": "number", "default": 0.0},
        },
        "required": ["total_debt", "gross_asset_value"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def loan_to_value_reit(
    total_debt: float,
    gross_asset_value: float,
    cash_and_restricted: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return LTV metrics including net debt adjustments."""
    try:
        gross_ltv = total_debt / gross_asset_value * 100 if gross_asset_value else 0.0
        net_ltv = (total_debt - cash_and_restricted) / gross_asset_value * 100 if gross_asset_value else 0.0
        data = {
            "gross_ltv_pct": round(gross_ltv, 2),
            "net_ltv_pct": round(net_ltv, 2),
            "liquidity_buffer_pct": round(cash_and_restricted / gross_asset_value * 100, 2) if gross_asset_value else 0.0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("loan_to_value_reit", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
