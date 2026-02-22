"""Model private equity distribution waterfalls across styles."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "distribution_waterfall_modeler",
    "description": "Calculates LP/GP outcomes for American and European waterfalls with tier detail.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "style": {"type": "string", "enum": ["american", "european"]},
            "total_commitments": {"type": "number"},
            "contributions": {"type": "array", "items": {"type": "object"}},
            "distributions": {"type": "array", "items": {"type": "object"}},
            "preferred_return_pct": {"type": "number", "default": 8.0},
            "gp_carry_pct": {"type": "number", "default": 20.0},
            "catch_up_pct": {"type": "number", "default": 100.0},
            "gp_commitment_pct": {"type": "number", "default": 2.0},
            "tiers": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["style", "total_commitments", "contributions", "distributions"],
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


def distribution_waterfall_modeler(
    style: str,
    total_commitments: float,
    contributions: list[dict[str, Any]],
    distributions: list[dict[str, Any]],
    preferred_return_pct: float = 8.0,
    gp_carry_pct: float = 20.0,
    catch_up_pct: float = 100.0,
    gp_commitment_pct: float = 2.0,
    tiers: list[dict[str, Any]] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return LP/GP cash flows, IRR, and tier breakdown for a fund waterfall."""
    try:
        style = style.lower()
        if style not in {"american", "european"}:
            raise ValueError("style must be american or european")
        cashflows = _build_cashflows(contributions, distributions)
        total_contrib = sum(item["amount"] for item in contributions)
        total_distr = sum(item["amount"] for item in distributions)
        life_years = max(_years_span(contributions + distributions), 1.0)
        pref_rate = preferred_return_pct / 100
        gp_commitment = total_commitments * (gp_commitment_pct / 100)
        roc = min(total_distr, total_contrib)
        pref = min(max(total_distr - roc, 0.0), total_contrib * pref_rate * life_years)
        catch_up_share = min(max(total_distr - roc - pref, 0.0), pref * (catch_up_pct / 100))
        residual = max(total_distr - roc - pref - catch_up_share, 0.0)
        gp_carry = residual * (gp_carry_pct / 100)
        lp_residual = residual - gp_carry
        lp_total = roc + pref + lp_residual
        gp_return_of_capital = gp_commitment + catch_up_share + gp_carry
        irr = _irr(cashflows)
        moic = (lp_total + gp_return_of_capital) / total_contrib if total_contrib else 0.0
        tier_breakdown = [
            {"tier": "return_of_capital", "amount": roc},
            {"tier": "preferred_return", "amount": pref},
            {"tier": "gp_catch_up", "amount": catch_up_share},
            {"tier": "residual", "amount": residual},
        ]
        if tiers:
            extra = []
            running_value = residual
            for tier in tiers:
                carry = tier.get("carry_pct", gp_carry_pct)
                threshold = tier.get("threshold_irr", 0)
                extra.append({"threshold_irr": threshold, "carry_pct": carry, "residual_pool": running_value})
            tier_breakdown.extend(extra)
        waterfall_table = [
            {"date": item["date"], "type": item["type"], "amount": item["amount"]}
            for item in cashflows
        ]
        data = {
            "lp_total": round(lp_total, 2),
            "gp_carry": round(gp_carry, 2),
            "gp_return_of_capital": round(gp_return_of_capital, 2),
            "irr": round(irr, 4),
            "moic": round(moic, 3),
            "tier_breakdown": tier_breakdown,
            "waterfall_table": waterfall_table,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("distribution_waterfall_modeler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_cashflows(events: list[dict[str, Any]], distributions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cashflows: list[dict[str, Any]] = []
    for record in events:
        cashflows.append(
            {
                "date": record.get("date"),
                "type": "contribution",
                "amount": -abs(float(record.get("amount", 0.0))),
            }
        )
    for record in distributions:
        cashflows.append(
            {
                "date": record.get("date"),
                "type": "distribution",
                "amount": abs(float(record.get("amount", 0.0))),
            }
        )
    cashflows.sort(key=lambda item: item.get("date", ""))
    return cashflows


def _years_span(events: list[dict[str, Any]]) -> float:
    dates = []
    for record in events:
        date_str = record.get("date")
        if not date_str:
            continue
        try:
            dates.append(datetime.fromisoformat(date_str))
        except ValueError:
            continue
    if not dates:
        return 1.0
    days = (max(dates) - min(dates)).days
    return max(days / 365.0, 1.0)


def _irr(cashflows: list[dict[str, Any]]) -> float:
    if not cashflows:
        return 0.0
    amounts = [entry["amount"] for entry in cashflows]
    guess_low, guess_high = -0.99, 1.5
    for _ in range(100):
        mid = (guess_low + guess_high) / 2
        npv = sum(amount / ((1 + mid) ** idx) for idx, amount in enumerate(amounts))
        if abs(npv) < 1e-4:
            return mid
        if npv > 0:
            guess_low = mid
        else:
            guess_high = mid
    return mid


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
