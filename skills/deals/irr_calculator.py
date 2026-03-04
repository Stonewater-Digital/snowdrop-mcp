"""Solve Internal Rate of Return using Newton's method."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "irr_calculator",
    "description": "Computes IRR, MOIC, and profit metrics from dated cash flows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash_flows": {
                "type": "array",
                "items": {"type": "object"},
                "description": "List of dicts with date (ISO) and amount (negative=outflow).",
            }
        },
        "required": ["cash_flows"],
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


def irr_calculator(cash_flows: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return annualized IRR and supporting metrics."""
    try:
        if len(cash_flows) < 2:
            raise ValueError("At least two cash flows required")

        normalized = _normalize_flows(cash_flows)
        amounts = [cf["amount"] for cf in normalized]
        if all(amount >= 0 for amount in amounts) or all(amount <= 0 for amount in amounts):
            raise ValueError("Cash flows must include both investments and returns")

        irr = _newton_solve(normalized)
        total_invested = abs(sum(amount for amount in amounts if amount < 0))
        total_returned = sum(amount for amount in amounts if amount > 0)
        moic = total_returned / total_invested if total_invested else 0
        net_profit = total_returned - total_invested
        data = {
            "irr_annual": round(irr, 4),
            "moic": round(moic, 3),
            "total_invested": round(total_invested, 2),
            "total_returned": round(total_returned, 2),
            "net_profit": round(net_profit, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("irr_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _normalize_flows(cash_flows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normal: list[dict[str, Any]] = []
    anchor: datetime | None = None
    for cf in cash_flows:
        dt = datetime.fromisoformat(str(cf.get("date"))).replace(tzinfo=timezone.utc)
        if anchor is None:
            anchor = dt
        delta_years = (dt - anchor).days / 365.0
        normal.append({"years": delta_years, "amount": float(cf.get("amount", 0.0))})
    return sorted(normal, key=lambda cf: cf["years"])


def _newton_solve(cash_flows: list[dict[str, Any]]) -> float:
    rate = 0.1
    for _ in range(100):
        npv, derivative = _npv_and_derivative(rate, cash_flows)
        if abs(derivative) < 1e-9:
            break
        new_rate = rate - npv / derivative
        if abs(new_rate - rate) < 1e-7:
            rate = new_rate
            break
        rate = max(new_rate, -0.999)
    return rate


def _npv_and_derivative(rate: float, cash_flows: list[dict[str, Any]]) -> tuple[float, float]:
    npv = 0.0
    derivative = 0.0
    for cf in cash_flows:
        years = cf["years"]
        amount = cf["amount"]
        discount = (1 + rate) ** years if years else 1.0
        npv += amount / discount
        if years:
            derivative -= years * amount / ((1 + rate) ** (years + 1))
    return npv, derivative


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
