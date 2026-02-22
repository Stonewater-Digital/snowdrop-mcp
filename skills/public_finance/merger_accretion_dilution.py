"""Perform merger accretion/dilution analysis."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "merger_accretion_dilution",
    "description": "Evaluates EPS impact of an acquisition with cash/stock mix and synergies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "acquirer": {"type": "object"},
            "target": {"type": "object"},
            "offer_premium_pct": {"type": "number"},
            "payment_mix": {"type": "object"},
            "synergies": {"type": "number"},
            "financing_rate": {"type": "number"},
            "tax_rate": {"type": "number"},
        },
        "required": ["acquirer", "target", "offer_premium_pct", "payment_mix", "synergies", "financing_rate", "tax_rate"],
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


def merger_accretion_dilution(
    acquirer: dict[str, Any],
    target: dict[str, Any],
    offer_premium_pct: float,
    payment_mix: dict[str, float],
    synergies: float,
    financing_rate: float,
    tax_rate: float,
    **_: Any,
) -> dict[str, Any]:
    """Return pro-forma EPS and accretion/dilution metrics."""
    try:
        base_price = target.get("share_price", 0.0)
        offer_price = base_price * (1 + offer_premium_pct / 100)
        deal_value = offer_price * target.get("shares_outstanding", 0.0)
        cash_pct = payment_mix.get("cash_pct", 0.0)
        stock_pct = payment_mix.get("stock_pct", 0.0)
        cash_needed = deal_value * cash_pct
        new_shares = (deal_value * stock_pct) / acquirer.get("share_price", 1.0)
        interest_expense = cash_needed * financing_rate * (1 - tax_rate)
        combined_net_income = (
            acquirer.get("eps", 0.0) * acquirer.get("shares_outstanding", 0.0)
            + target.get("eps", 0.0) * target.get("shares_outstanding", 0.0)
            + synergies
            - interest_expense
        )
        proforma_shares = acquirer.get("shares_outstanding", 0.0) + new_shares
        proforma_eps = combined_net_income / proforma_shares if proforma_shares else 0.0
        accretion = (proforma_eps - acquirer.get("eps", 0.0)) / acquirer.get("eps", 0.0) if acquirer.get("eps", 0.0) else 0.0
        break_even_synergies = max(interest_expense - target.get("eps", 0.0) * target.get("shares_outstanding", 0.0), 0.0)
        data = {
            "accretive": accretion >= 0,
            "proforma_eps": round(proforma_eps, 3),
            "acquirer_standalone_eps": acquirer.get("eps"),
            "accretion_dilution_pct": round(accretion * 100, 2),
            "break_even_synergies": round(break_even_synergies, 2),
            "deal_value": round(deal_value, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("merger_accretion_dilution", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
