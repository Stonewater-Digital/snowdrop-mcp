"""Calculate producer breakeven oil price."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "oil_breakeven_price_calculator",
    "description": (
        "Determines the breakeven oil price for an upstream producer including lifting costs, "
        "opex, sustaining capex, royalties, production taxes, and a target return margin. "
        "Supports both simple and government-take deduction methods."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "lifting_cost_per_bbl": {
                "type": "number",
                "description": "Direct lifting/extraction cost per barrel (must be >= 0).",
            },
            "opex_per_bbl": {
                "type": "number",
                "description": "Operating expenditure per barrel excluding lifting (must be >= 0).",
            },
            "sustaining_capex_per_bbl": {
                "type": "number",
                "default": 0.0,
                "description": "Sustaining capital expenditure per barrel (must be >= 0).",
            },
            "royalty_pct": {
                "type": "number",
                "default": 5.0,
                "description": "Royalty rate as % of gross revenue (0–100). Defaults to 5%.",
            },
            "tax_pct": {
                "type": "number",
                "default": 20.0,
                "description": "Production tax / corporate tax rate as % of net revenue (0–100). Defaults to 20%.",
            },
            "target_margin_pct": {
                "type": "number",
                "default": 0.0,
                "description": "Required return margin as % of breakeven price (0–100). Defaults to 0.",
            },
        },
        "required": ["lifting_cost_per_bbl", "opex_per_bbl"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "cost_base_per_bbl": {"type": "number"},
            "breakeven_price_per_bbl": {"type": "number"},
            "government_take_pct": {"type": "number"},
            "net_producer_share_pct": {"type": "number"},
            "timestamp": {"type": "string"},
        },
    },
}


def oil_breakeven_price_calculator(
    lifting_cost_per_bbl: float,
    opex_per_bbl: float,
    sustaining_capex_per_bbl: float = 0.0,
    royalty_pct: float = 5.0,
    tax_pct: float = 20.0,
    target_margin_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return the minimum oil price required to cover full cost stack plus target return.

    Args:
        lifting_cost_per_bbl: Direct extraction cost per barrel.
        opex_per_bbl: Operating cost per barrel (G&A, maintenance, etc.).
        sustaining_capex_per_bbl: Capital needed to maintain current production.
        royalty_pct: Revenue royalty taken off the top (% of gross price).
        tax_pct: Production/corporate tax on net revenue (% of after-royalty revenue).
        target_margin_pct: Required profit margin as % of price above breakeven.

    Returns:
        dict with status, cost_base_per_bbl, breakeven_price_per_bbl,
        government_take_pct, and net_producer_share_pct.

    Formula:
        cost_base = lifting_cost + opex + sustaining_capex
        take_rate  = 1 - (royalty_pct + tax_pct + target_margin_pct) / 100
        breakeven  = cost_base / take_rate

    The government take (royalty + tax) is applied sequentially to revenue,
    so breakeven = cost_base / (1 - effective_deduction_rate).
    Combined royalty + tax must be < 100%; if > 100% raises ValueError.
    """
    try:
        if lifting_cost_per_bbl < 0:
            raise ValueError("lifting_cost_per_bbl must be non-negative")
        if opex_per_bbl < 0:
            raise ValueError("opex_per_bbl must be non-negative")
        if sustaining_capex_per_bbl < 0:
            raise ValueError("sustaining_capex_per_bbl must be non-negative")
        if not (0 <= royalty_pct < 100):
            raise ValueError("royalty_pct must be in [0, 100)")
        if not (0 <= tax_pct < 100):
            raise ValueError("tax_pct must be in [0, 100)")
        total_deduction = royalty_pct + tax_pct + target_margin_pct
        if total_deduction >= 100:
            raise ValueError(
                f"Combined royalty ({royalty_pct}%) + tax ({tax_pct}%) + "
                f"margin ({target_margin_pct}%) = {total_deduction}% must be < 100%"
            )

        cost_base = lifting_cost_per_bbl + opex_per_bbl + sustaining_capex_per_bbl
        take_rate = 1.0 - total_deduction / 100.0
        breakeven = cost_base / take_rate

        government_take = royalty_pct + tax_pct
        net_producer_share = 100.0 - government_take

        return {
            "status": "success",
            "cost_base_per_bbl": round(cost_base, 2),
            "breakeven_price_per_bbl": round(breakeven, 2),
            "government_take_pct": round(government_take, 2),
            "net_producer_share_pct": round(net_producer_share, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("oil_breakeven_price_calculator", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
