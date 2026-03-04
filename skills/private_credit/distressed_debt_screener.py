"""Screen credits for distress indicators."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "distressed_debt_screener",
    "description": "Flags distressed signals using price, spread, PD, and coverage metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "price_pct_of_par": {"type": "number"},
            "spread_bps": {"type": "number"},
            "prob_default_pct": {"type": "number"},
            "interest_coverage": {"type": "number"},
        },
        "required": ["price_pct_of_par", "spread_bps", "prob_default_pct", "interest_coverage"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def distressed_debt_screener(
    price_pct_of_par: float,
    spread_bps: float,
    prob_default_pct: float,
    interest_coverage: float,
    **_: Any,
) -> dict[str, Any]:
    """Return distress flags and composite risk score."""
    try:
        price_flag = price_pct_of_par < 80
        spread_flag = spread_bps > 800
        pd_flag = prob_default_pct > 10
        coverage_flag = interest_coverage < 1.0
        score = 0
        score += 2 if price_flag else 0
        score += 2 if spread_flag else 0
        score += 1 if pd_flag else 0
        score += 1 if coverage_flag else 0
        data = {
            "distress_score": score,
            "signals": {
                "price": price_flag,
                "spread": spread_flag,
                "prob_default": pd_flag,
                "interest_coverage": coverage_flag,
            },
            "high_risk": score >= 4,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("distressed_debt_screener", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
