"""Analyze private credit term sheet economics and protections."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "private_credit_term_analyzer",
    "description": "Computes all-in yields, covenant protection, and risk assessment for private credit facilities.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "facility": {"type": "object"},
        },
        "required": ["facility"],
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


def private_credit_term_analyzer(facility: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return yield, covenant, and risk diagnostics for a term sheet."""
    try:
        commitment = float(facility.get("commitment", 0.0))
        drawn = float(facility.get("drawn", commitment))
        spread_bps = int(facility.get("spread_bps", 0))
        floor_bps = int(facility.get("floor_bps", 0))
        oid_pct = float(facility.get("oid_pct", 0.0))
        maturity = int(facility.get("maturity_years", 5))
        base_rate = 0.05 if facility.get("base_rate", "SOFR").lower() == "sofr" else 0.08
        call_protection = facility.get("call_protection", []) or []
        covenants = facility.get("covenants", []) or []

        all_in_yield = base_rate + spread_bps / 10000 + floor_bps / 10000 + oid_pct / maturity
        effective_cost = all_in_yield * drawn / max(drawn, 1)
        spread_to_benchmark = spread_bps + floor_bps
        weighted_average_life = maturity * 0.6 if facility.get("type") in {"unitranche", "second_lien"} else maturity * 0.5

        covenant_analysis = []
        for covenant in covenants:
            metric = covenant.get("metric")
            threshold = covenant.get("threshold")
            headroom = covenant.get("current") - threshold if covenant.get("direction") == "min" else threshold - covenant.get("current")
            covenant_analysis.append(
                {
                    "name": covenant.get("name", metric),
                    "metric": metric,
                    "threshold": threshold,
                    "current": covenant.get("current"),
                    "headroom": headroom,
                }
            )
        call_value = sum(item.get("premium_pct", 0) for item in call_protection) * commitment / 100
        missing_cov = ["maintenance leverage", "fixed charge coverage"]
        protections = len([c for c in covenants if c.get("type") == "maintenance"])
        risk_score = 80 - protections * 5 - (spread_to_benchmark / 100)
        risk_score = max(min(risk_score, 100), 0)
        data = {
            "all_in_yield": round(all_in_yield, 4),
            "effective_annual_cost": round(effective_cost, 4),
            "spread_to_benchmark": spread_to_benchmark,
            "covenant_analysis": covenant_analysis,
            "call_protection_value_est": round(call_value, 2),
            "risk_assessment": "low" if risk_score > 70 else "high" if risk_score < 40 else "moderate",
            "weighted_average_life": round(weighted_average_life, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("private_credit_term_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
