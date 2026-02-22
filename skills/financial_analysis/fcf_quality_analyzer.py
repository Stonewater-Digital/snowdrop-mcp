"""Assess free cash flow quality versus net income."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "fcf_quality_analyzer",
    "description": "Compares free cash flow to net income and highlights working capital effects.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {"type": "number"},
            "operating_cash_flow": {"type": "number"},
            "capex": {"type": "number"},
            "depreciation": {"type": "number"},
            "stock_comp": {"type": "number"},
            "change_in_receivables": {"type": "number"},
            "change_in_payables": {"type": "number"},
            "change_in_inventory": {"type": "number"},
        },
        "required": [
            "net_income",
            "operating_cash_flow",
            "capex",
            "depreciation",
            "stock_comp",
            "change_in_receivables",
            "change_in_payables",
            "change_in_inventory",
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


def fcf_quality_analyzer(
    net_income: float,
    operating_cash_flow: float,
    capex: float,
    depreciation: float,
    stock_comp: float,
    change_in_receivables: float,
    change_in_payables: float,
    change_in_inventory: float,
    **_: Any,
) -> dict[str, Any]:
    """Return FCF, quality metrics, and red flags."""
    try:
        fcf = operating_cash_flow - capex
        ratio = fcf / max(net_income, 1e-6)
        adjustments = [
            {"item": "Stock-based comp", "adjustment": -stock_comp},
            {"item": "Receivables", "adjustment": -change_in_receivables},
            {"item": "Payables", "adjustment": change_in_payables},
            {"item": "Inventory", "adjustment": -change_in_inventory},
        ]
        quality_score = max(min(ratio, 2), -2)
        red_flags = []
        if ratio < 0.8:
            red_flags.append("FCF trails net income materially")
        if change_in_receivables < 0 and change_in_payables > 0:
            red_flags.append("Sales growth funded via working capital stretch")
        assessment = "healthy" if ratio > 1 else "mixed" if ratio > 0.5 else "poor"
        data = {
            "fcf": round(fcf, 2),
            "fcf_to_ni_ratio": round(ratio, 2),
            "quality_score": round(quality_score, 2),
            "adjustments": adjustments,
            "red_flags": red_flags,
            "assessment": assessment,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("fcf_quality_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
