"""Model CECL-style expected credit losses for loan portfolios."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "loan_loss_reserve_modeler",
    "description": "Calculates expected credit losses by segment with macro overlays.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "loan_portfolio": {"type": "array", "items": {"type": "object"}},
            "macro_adjustment": {"type": "number", "default": 1.0},
        },
        "required": ["loan_portfolio"],
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


def loan_loss_reserve_modeler(
    loan_portfolio: list[dict[str, Any]],
    macro_adjustment: float = 1.0,
    **_: Any,
) -> dict[str, Any]:
    """Return ECL by segment and total reserve ratio."""
    try:
        if not loan_portfolio:
            raise ValueError("loan_portfolio cannot be empty")
        by_segment = []
        total_balance = 0.0
        total_reserve = 0.0
        for segment in loan_portfolio:
            balance = float(segment.get("balance", 0))
            pd = float(segment.get("pd_annual", 0))
            lgd = float(segment.get("lgd", 0))
            remaining_life = float(segment.get("remaining_life_years", 1))
            ecl = balance * pd * lgd * remaining_life * macro_adjustment
            by_segment.append(
                {
                    "segment": segment.get("segment"),
                    "balance": balance,
                    "expected_loss": round(ecl, 2),
                }
            )
            total_balance += balance
            total_reserve += ecl
        reserve_ratio = total_reserve / max(total_balance, 1e-6) * 100
        adequacy = "adequate" if reserve_ratio >= 1.5 else "needs_build"
        data = {
            "total_reserve": round(total_reserve, 2),
            "reserve_ratio_pct": round(reserve_ratio, 2),
            "by_segment": by_segment,
            "adequacy_assessment": adequacy,
            "macro_sensitivity": {
                "base": round(total_reserve, 2),
                "+10%": round(total_reserve * 1.1, 2),
                "-10%": round(total_reserve * 0.9, 2),
            },
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("loan_loss_reserve_modeler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
