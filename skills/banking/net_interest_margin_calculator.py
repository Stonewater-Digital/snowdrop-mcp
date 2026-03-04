"""Analyze bank net interest margin and rate sensitivity."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "net_interest_margin_calculator",
    "description": "Computes current NIM, gap ratios, and projected NIM under rate shocks.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "interest_income": {"type": "number"},
            "interest_expense": {"type": "number"},
            "earning_assets": {"type": "number"},
            "rate_environment": {
                "type": "string",
                "enum": ["rising", "falling", "stable"],
            },
            "asset_repricing_pct": {"type": "number"},
            "liability_repricing_pct": {"type": "number"},
        },
        "required": [
            "interest_income",
            "interest_expense",
            "earning_assets",
            "rate_environment",
            "asset_repricing_pct",
            "liability_repricing_pct",
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


def net_interest_margin_calculator(
    interest_income: float,
    interest_expense: float,
    earning_assets: float,
    rate_environment: str,
    asset_repricing_pct: float,
    liability_repricing_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return NIM, spread, sensitivity gap, and projected rate-shock outcomes."""
    try:
        if earning_assets <= 0:
            raise ValueError("earning_assets must be positive")
        nim = (interest_income - interest_expense) / earning_assets
        spread = interest_income / earning_assets - interest_expense / earning_assets
        gap_ratio = asset_repricing_pct / max(liability_repricing_pct, 0.01)
        delta = 0.01
        nim_plus = nim + (asset_repricing_pct - liability_repricing_pct) / 100 * delta
        nim_minus = nim - (asset_repricing_pct - liability_repricing_pct) / 100 * delta
        asset_sensitive = gap_ratio > 1
        recommendation = "Shorten asset duration" if asset_sensitive and rate_environment == "falling" else "Extend liabilities" if not asset_sensitive and rate_environment == "rising" else "Maintain positioning"
        data = {
            "nim_pct": round(nim * 100, 3),
            "spread": round(spread * 100, 3),
            "gap_ratio": round(gap_ratio, 2),
            "nim_at_plus_100bps": round(nim_plus * 100, 3),
            "nim_at_minus_100bps": round(nim_minus * 100, 3),
            "asset_sensitive": asset_sensitive,
            "recommendation": recommendation,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("net_interest_margin_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
