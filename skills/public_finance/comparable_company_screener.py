"""Screen comparable companies and compute valuation multiples."""
from __future__ import annotations

from statistics import mean, median
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "comparable_company_screener",
    "description": "Calculates EV/Revenue, EV/EBITDA, P/E, and implied values for a target.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "target": {"type": "object"},
            "comps": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["target", "comps"],
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


def comparable_company_screener(target: dict[str, Any], comps: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return comp tables and implied target valuation."""
    try:
        comp_table = []
        ev_rev, ev_ebitda, pe = [], [], []
        for comp in comps:
            ev = comp.get("share_price", 0.0) * comp.get("shares_outstanding", 0.0) + comp.get("total_debt", 0.0) - comp.get("cash", 0.0)
            rev_multiple = ev / comp.get("revenue", 1)
            ebitda_multiple = ev / comp.get("ebitda", 1)
            pe_multiple = (comp.get("share_price", 0.0) / (comp.get("eps", comp.get("net_income", 1) / comp.get("shares_outstanding", 1)))) if comp.get("shares_outstanding") else 0.0
            comp_table.append(
                {
                    "name": comp.get("name"),
                    "enterprise_value": round(ev, 2),
                    "ev_revenue": round(rev_multiple, 2),
                    "ev_ebitda": round(ebitda_multiple, 2),
                    "pe": round(pe_multiple, 2),
                }
            )
            ev_rev.append(rev_multiple)
            ev_ebitda.append(ebitda_multiple)
            pe.append(pe_multiple)
        median_multiples = {
            "ev_revenue": round(median(ev_rev), 2),
            "ev_ebitda": round(median(ev_ebitda), 2),
            "pe": round(median(pe), 2),
        }
        mean_multiples = {
            "ev_revenue": round(mean(ev_rev), 2),
            "ev_ebitda": round(mean(ev_ebitda), 2),
            "pe": round(mean(pe), 2),
        }
        implied_ev = median_multiples["ev_ebitda"] * target.get("ebitda", 0.0)
        implied_equity = implied_ev - target.get("total_debt", 0.0) + target.get("cash", 0.0)
        implied_price = implied_equity / target.get("shares_outstanding", 1) if target.get("shares_outstanding") else 0.0
        closest_comp = max(comp_table, key=lambda row: row["ev_ebitda"], default={}).get("name")
        data = {
            "comp_table": comp_table,
            "median_multiples": median_multiples,
            "mean_multiples": mean_multiples,
            "implied_target_values": {"enterprise_value": round(implied_ev, 2), "equity_value": round(implied_equity, 2), "per_share": round(implied_price, 2)},
            "target_percentile": {
                "ev_ebitda": sum(1 for multiple in ev_ebitda if multiple <= implied_ev) / len(ev_ebitda) if ev_ebitda else 0.0,
            },
            "closest_comp": closest_comp,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("comparable_company_screener", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
