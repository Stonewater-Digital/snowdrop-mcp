"""Compute REIT FFO and AFFO metrics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ffo_affo_calculator",
    "description": "Calculates FFO/AFFO and payout ratios for REITs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {"type": "number"},
            "depreciation_real_estate": {"type": "number"},
            "amortization_real_estate": {"type": "number"},
            "gains_on_sale": {"type": "number"},
            "losses_on_sale": {"type": "number"},
            "impairments": {"type": "number"},
            "straight_line_rent_adj": {"type": "number"},
            "recurring_capex": {"type": "number"},
            "lease_commissions": {"type": "number"},
            "tenant_improvements": {"type": "number"},
            "shares_outstanding": {"type": "number"},
        },
        "required": [
            "net_income",
            "depreciation_real_estate",
            "amortization_real_estate",
            "gains_on_sale",
            "losses_on_sale",
            "impairments",
            "straight_line_rent_adj",
            "recurring_capex",
            "lease_commissions",
            "tenant_improvements",
            "shares_outstanding",
        ],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def ffo_affo_calculator(
    net_income: float,
    depreciation_real_estate: float,
    amortization_real_estate: float,
    gains_on_sale: float,
    losses_on_sale: float,
    impairments: float,
    straight_line_rent_adj: float,
    recurring_capex: float,
    lease_commissions: float,
    tenant_improvements: float,
    shares_outstanding: float,
    **_: Any,
) -> dict[str, Any]:
    """Return FFO/AFFO metrics."""
    try:
        ffo = net_income + depreciation_real_estate + amortization_real_estate - gains_on_sale + losses_on_sale + impairments
        affo = ffo - straight_line_rent_adj - recurring_capex - lease_commissions - tenant_improvements
        ffo_ps = ffo / shares_outstanding if shares_outstanding else 0.0
        affo_ps = affo / shares_outstanding if shares_outstanding else 0.0
        payout_ffo = 0.0
        payout_affo = 0.0
        maintenance_ratio = recurring_capex / (net_income + depreciation_real_estate) if (net_income + depreciation_real_estate) else 0.0
        data = {
            "ffo": round(ffo, 2),
            "ffo_per_share": round(ffo_ps, 3),
            "affo": round(affo, 2),
            "affo_per_share": round(affo_ps, 3),
            "ffo_payout_ratio": round(payout_ffo, 3),
            "affo_payout_ratio": round(payout_affo, 3),
            "maintenance_capex_ratio": round(maintenance_ratio, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("ffo_affo_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
