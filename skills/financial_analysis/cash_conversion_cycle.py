"""Analyze cash conversion cycles."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cash_conversion_cycle",
    "description": "Computes DSO, DIO, DPO, and the cash conversion cycle to assess working capital efficiency.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "revenue": {"type": "number"},
            "cogs": {"type": "number"},
            "receivables": {"type": "number"},
            "inventory": {"type": "number"},
            "payables": {"type": "number"},
            "prior_receivables": {"type": "number"},
            "prior_inventory": {"type": "number"},
            "prior_payables": {"type": "number"},
        },
        "required": [
            "revenue",
            "cogs",
            "receivables",
            "inventory",
            "payables",
            "prior_receivables",
            "prior_inventory",
            "prior_payables",
        ],
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


def cash_conversion_cycle(
    revenue: float,
    cogs: float,
    receivables: float,
    inventory: float,
    payables: float,
    prior_receivables: float,
    prior_inventory: float,
    prior_payables: float,
    **_: Any,
) -> dict[str, Any]:
    """Return CCC metrics and efficiency assessment."""
    try:
        avg_receivables = (receivables + prior_receivables) / 2
        avg_inventory = (inventory + prior_inventory) / 2
        avg_payables = (payables + prior_payables) / 2
        dso = (avg_receivables / max(revenue, 1e-6)) * 365
        dio = (avg_inventory / max(cogs, 1e-6)) * 365
        dpo = (avg_payables / max(cogs, 1e-6)) * 365
        ccc = dso + dio - dpo
        efficiency = "efficient" if ccc < 60 else "neutral" if ccc < 120 else "stressed"
        trend_note = "Improving" if receivables <= prior_receivables else "Worsening"
        cash_tied = cogs / 365 * max(ccc, 0)
        data = {
            "ccc_days": round(ccc, 2),
            "dso": round(dso, 2),
            "dio": round(dio, 2),
            "dpo": round(dpo, 2),
            "trend_note": trend_note,
            "working_capital_efficiency": efficiency,
            "cash_tied_up_estimate": round(cash_tied, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("cash_conversion_cycle", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
