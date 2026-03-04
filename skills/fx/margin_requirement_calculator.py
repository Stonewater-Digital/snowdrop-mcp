"""Calculate margin requirement for a forex position.

MCP Tool Name: margin_requirement_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "margin_requirement_calculator",
    "description": "Calculate the margin required to open a forex position given position size and leverage. margin = position_size / leverage.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "position_size": {
                "type": "number",
                "description": "Total position size in account currency.",
            },
            "leverage": {
                "type": "number",
                "description": "Leverage ratio (e.g. 50 for 50:1 leverage).",
                "default": 50,
            },
        },
        "required": ["position_size"],
    },
}


def margin_requirement_calculator(
    position_size: float,
    leverage: float = 50,
) -> dict[str, Any]:
    """Calculate margin requirement."""
    try:
        if position_size <= 0:
            return {
                "status": "error",
                "data": {"error": "position_size must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if leverage <= 0:
            return {
                "status": "error",
                "data": {"error": "leverage must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        margin = position_size / leverage
        margin_pct = 1 / leverage * 100

        # Common leverage tiers
        tiers = [
            (500, "Very high — typically for major pairs in some offshore brokers"),
            (200, "High — common in EU/AU for major pairs"),
            (100, "Standard — many brokers default"),
            (50, "US retail forex maximum (CFTC regulation)"),
            (30, "ESMA retail maximum for major pairs"),
            (20, "ESMA retail for minor pairs"),
            (2, "US equity margin (Reg T)"),
        ]
        tier_note = ""
        for tier_lev, note in tiers:
            if leverage >= tier_lev:
                tier_note = note
                break

        return {
            "status": "ok",
            "data": {
                "position_size": round(position_size, 2),
                "leverage": f"{leverage}:1",
                "margin_required": round(margin, 2),
                "margin_pct": round(margin_pct, 4),
                "leverage_note": tier_note,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
