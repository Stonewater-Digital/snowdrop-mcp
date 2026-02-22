"""
Executive Summary: Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers.

Inputs: fund_size (float), preferred_return (float), carry_rate (float), gp_commitment (float), distribution_amount (float)
Outputs: dict with lp_share (float), gp_share (float), carry (float), breakdown_table (list[dict])
MCP Tool Name: calc_waterfall_dist
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "calc_waterfall_dist",
    "description": "Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_size": {"type": "number", "description": "Total fund size in dollars"},
            "preferred_return": {"type": "number", "description": "Preferred return rate for LPs (e.g. 0.08 for 8%)"},
            "carry_rate": {"type": "number", "description": "GP carried interest rate (e.g. 0.20 for 20%)"},
            "gp_commitment": {"type": "number", "description": "GP capital commitment in dollars"},
            "distribution_amount": {"type": "number", "description": "Total distribution amount available in dollars"},
        },
        "required": ["fund_size", "preferred_return", "carry_rate", "gp_commitment", "distribution_amount"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "lp_share": {"type": "number"},
            "gp_share": {"type": "number"},
            "carry": {"type": "number"},
            "breakdown_table": {"type": "array", "items": {"type": "object"}},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["lp_share", "gp_share", "carry", "breakdown_table", "status", "timestamp"],
    },
}


def calc_waterfall_dist(
    fund_size: float,
    preferred_return: float,
    carry_rate: float,
    gp_commitment: float,
    distribution_amount: float,
    **kwargs: Any,
) -> dict:
    """Calculates LP/GP waterfall distributions across tiered hurdle structure.

    Implements the standard American waterfall:
    1. Return of capital to LPs and GP (pro-rata)
    2. Preferred return to LPs on LP capital
    3. GP catch-up (GP receives carry_rate of total until caught up)
    4. Remaining split: (1 - carry_rate) to LPs, carry_rate to GP

    Args:
        fund_size: Total fund size in dollars.
        preferred_return: Annual preferred return rate for LPs (e.g. 0.08).
        carry_rate: GP carried interest rate (e.g. 0.20).
        gp_commitment: GP capital commitment in dollars.
        distribution_amount: Total distribution amount available in dollars.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Keys include lp_share (float), gp_share (float), carry (float),
              breakdown_table (list of dicts per tier), status, and timestamp.
    """
    try:
        lp_commitment = fund_size - gp_commitment
        lp_pct = lp_commitment / fund_size if fund_size > 0 else 0.0
        gp_pct = gp_commitment / fund_size if fund_size > 0 else 0.0

        remaining = distribution_amount
        lp_share = 0.0
        gp_share = 0.0
        carry = 0.0
        breakdown_table: list[dict] = []

        # Tier 1: Return of capital (pro-rata LP/GP)
        roc_available = min(remaining, fund_size)
        lp_roc = roc_available * lp_pct
        gp_roc = roc_available * gp_pct
        lp_share += lp_roc
        gp_share += gp_roc
        remaining -= roc_available
        breakdown_table.append({
            "tier": "1_return_of_capital",
            "total": round(roc_available, 2),
            "lp": round(lp_roc, 2),
            "gp": round(gp_roc, 2),
            "description": "Return of contributed capital pro-rata",
        })

        # Tier 2: Preferred return to LPs on LP capital
        lp_pref_amount = lp_commitment * preferred_return
        lp_pref_paid = min(remaining, lp_pref_amount)
        lp_share += lp_pref_paid
        remaining -= lp_pref_paid
        breakdown_table.append({
            "tier": "2_preferred_return",
            "total": round(lp_pref_paid, 2),
            "lp": round(lp_pref_paid, 2),
            "gp": 0.0,
            "description": f"Preferred return at {preferred_return:.1%} on LP capital of ${lp_commitment:,.2f}",
        })

        # Tier 3: GP catch-up
        # GP receives 100% until GP has received carry_rate of (preferred + catch-up)
        # Equation: catch_up = carry_rate * (lp_pref_paid + catch_up)
        # => catch_up * (1 - carry_rate) = carry_rate * lp_pref_paid
        # => catch_up = (carry_rate / (1 - carry_rate)) * lp_pref_paid
        if carry_rate < 1.0:
            catchup_needed = (carry_rate / (1.0 - carry_rate)) * lp_pref_paid
        else:
            catchup_needed = 0.0
        catchup_paid = min(remaining, catchup_needed)
        gp_share += catchup_paid
        carry += catchup_paid
        remaining -= catchup_paid
        breakdown_table.append({
            "tier": "3_gp_catchup",
            "total": round(catchup_paid, 2),
            "lp": 0.0,
            "gp": round(catchup_paid, 2),
            "description": f"GP catch-up at {carry_rate:.1%} carry until GP is caught up",
        })

        # Tier 4: Residual split
        lp_residual = remaining * (1.0 - carry_rate)
        gp_residual = remaining * carry_rate
        lp_share += lp_residual
        gp_share += gp_residual
        carry += gp_residual
        breakdown_table.append({
            "tier": "4_residual_split",
            "total": round(remaining, 2),
            "lp": round(lp_residual, 2),
            "gp": round(gp_residual, 2),
            "description": f"Residual: {(1 - carry_rate):.1%} LP / {carry_rate:.1%} GP (carry)",
        })

        result = {
            "lp_share": round(lp_share, 2),
            "gp_share": round(gp_share, 2),
            "carry": round(carry, 2),
            "breakdown_table": breakdown_table,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"calc_waterfall_dist failed: {e}")
        _log_lesson(f"calc_waterfall_dist: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
