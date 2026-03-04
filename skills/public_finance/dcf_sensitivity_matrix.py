"""DCF valuation with WACC/terminal growth sensitivity."""
from __future__ import annotations

from datetime import datetime, timezone
from statistics import median
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "dcf_sensitivity_matrix",
    "description": "Builds a DCF table across WACC and terminal growth assumptions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "free_cash_flows": {"type": "array", "items": {"type": "number"}},
            "wacc_range": {"type": "array", "items": {"type": "number"}},
            "terminal_growth_range": {"type": "array", "items": {"type": "number"}},
            "shares_outstanding": {"type": "number"},
            "net_debt": {"type": "number"},
        },
        "required": [
            "free_cash_flows",
            "wacc_range",
            "terminal_growth_range",
            "shares_outstanding",
            "net_debt",
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


def dcf_sensitivity_matrix(
    free_cash_flows: list[float],
    wacc_range: list[float],
    terminal_growth_range: list[float],
    shares_outstanding: float,
    net_debt: float,
    **_: Any,
) -> dict[str, Any]:
    """Return base case and sensitivity matrix for DCF valuation."""
    try:
        matrix: list[list[float]] = []
        prices = []
        for growth in terminal_growth_range:
            row = []
            for wacc in wacc_range:
                price = _dcf_price(free_cash_flows, wacc, growth, shares_outstanding, net_debt)
                row.append(round(price, 2))
                prices.append(price)
            matrix.append(row)
        base_case = {
            "wacc": wacc_range[len(wacc_range) // 2],
            "terminal_growth": terminal_growth_range[len(terminal_growth_range) // 2],
            "price": matrix[len(matrix) // 2][len(wacc_range) // 2],
        }
        data = {
            "base_case": base_case,
            "sensitivity_matrix": matrix,
            "wacc_labels": wacc_range,
            "growth_labels": terminal_growth_range,
            "min_price": round(min(prices), 2),
            "max_price": round(max(prices), 2),
            "median_price": round(median(prices), 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("dcf_sensitivity_matrix", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _dcf_price(cashflows: list[float], wacc: float, growth: float, shares: float, net_debt: float) -> float:
    discount = 0.0
    for idx, fcf in enumerate(cashflows, start=1):
        discount += fcf / ((1 + wacc) ** idx)
    terminal = cashflows[-1] * (1 + growth) / (wacc - growth)
    present_value = discount + terminal / ((1 + wacc) ** len(cashflows))
    equity_value = present_value - net_debt
    return equity_value / shares if shares else 0.0


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
