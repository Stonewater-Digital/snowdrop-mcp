"""Lifetime value calculations per agent tier."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ltv_calculator",
    "description": "Computes LTV, discounted LTV, and payback metrics for each agent tier.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "tier_metrics": {
                "type": "array",
                "items": {"type": "object"},
                "description": (
                    "List of tier dictionaries with tier, avg_monthly_revenue, avg_lifetime_months,"
                    " gross_margin_pct, and optional acquisition_cost."
                ),
            },
            "discount_rate_monthly": {
                "type": "number",
                "description": "Monthly discount rate used for present-value LTV.",
                "default": 0.01,
            },
        },
        "required": ["tier_metrics"],
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


def ltv_calculator(
    tier_metrics: list[dict[str, Any]],
    discount_rate_monthly: float = 0.01,
    **_: Any,
) -> dict[str, Any]:
    """Calculate LTV components for each tier."""
    try:
        if not isinstance(tier_metrics, list):
            raise ValueError("tier_metrics must be a list")
        if discount_rate_monthly < 0:
            raise ValueError("discount_rate_monthly cannot be negative")

        per_tier: list[dict[str, Any]] = []
        for entry in tier_metrics:
            if not isinstance(entry, dict):
                raise ValueError("Each tier metric must be a dict")
            try:
                tier = str(entry["tier"])
                arpu = float(entry["avg_monthly_revenue"])
                lifetime_months = float(entry["avg_lifetime_months"])
                margin_pct = float(entry["gross_margin_pct"])
            except KeyError as missing:
                raise ValueError(f"Missing field: {missing.args[0]}") from missing

            if lifetime_months <= 0:
                raise ValueError("avg_lifetime_months must be positive")
            if arpu < 0:
                raise ValueError("avg_monthly_revenue cannot be negative")

            if margin_pct > 1:
                margin_pct /= 100.0
            margin_pct = max(min(margin_pct, 1.0), 0.0)

            monthly_margin = arpu * margin_pct
            churn_rate = 1 / lifetime_months
            base_ltv = (monthly_margin / churn_rate) if churn_rate else 0.0

            if discount_rate_monthly > 0:
                discounted_factor = (1 - (1 + discount_rate_monthly) ** (-lifetime_months)) / discount_rate_monthly
                discounted_ltv = monthly_margin * discounted_factor
            else:
                discounted_ltv = monthly_margin * lifetime_months

            acquisition_cost = float(entry.get("acquisition_cost", 0.0) or 0.0)
            ltv_to_cac = (base_ltv / acquisition_cost) if acquisition_cost > 0 else None
            payback_period = (acquisition_cost / monthly_margin) if monthly_margin > 0 and acquisition_cost > 0 else None

            per_tier.append(
                {
                    "tier": tier,
                    "ltv": round(base_ltv, 2),
                    "discounted_ltv": round(discounted_ltv, 2),
                    "churn_rate": round(churn_rate, 4),
                    "ltv_to_cac": round(ltv_to_cac, 2) if ltv_to_cac is not None else None,
                    "payback_period_months": round(payback_period, 2) if payback_period is not None else None,
                }
            )

        result = {
            "per_tier": per_tier,
            "assumptions": {"discount_rate_monthly": discount_rate_monthly},
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("ltv_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
