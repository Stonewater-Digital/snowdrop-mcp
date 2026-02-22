"""
Executive Summary: Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance.

Inputs: assets (list[dict] with name/value), liabilities (float), shares_outstanding (float), prior_nav_per_share (float, optional)
Outputs: dict with nav_per_share (float), total_nav (float), variance_from_prior (float or null)
MCP Tool Name: nav_reconciliation
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "nav_reconciliation",
    "description": "Calculates fund Net Asset Value per share and reconciles against prior NAV, flagging variance.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assets": {
                "type": "array",
                "description": "List of asset objects with name and value fields",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "value": {"type": "number"},
                    },
                    "required": ["name", "value"],
                },
            },
            "liabilities": {"type": "number", "description": "Total liabilities in dollars"},
            "shares_outstanding": {"type": "number", "description": "Number of shares/units outstanding"},
            "prior_nav_per_share": {
                "type": "number",
                "description": "Prior period NAV per share for variance calculation (optional)",
            },
        },
        "required": ["assets", "liabilities", "shares_outstanding"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "nav_per_share": {"type": "number"},
            "total_nav": {"type": "number"},
            "variance_from_prior": {"type": ["number", "null"]},
            "variance_pct": {"type": ["number", "null"]},
            "total_assets": {"type": "number"},
            "asset_breakdown": {"type": "array"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["nav_per_share", "total_nav", "variance_from_prior", "status", "timestamp"],
    },
}


def nav_reconciliation(
    assets: list[dict[str, Any]],
    liabilities: float,
    shares_outstanding: float,
    prior_nav_per_share: float | None = None,
    **kwargs: Any,
) -> dict:
    """Calculates NAV per share and reconciles against prior period NAV.

    Sums all asset values, subtracts total liabilities to get total NAV,
    then divides by shares outstanding to compute NAV per share. If a
    prior NAV per share is provided, computes absolute and percentage variance.

    Args:
        assets: List of dicts, each with 'name' (str) and 'value' (float).
        liabilities: Total liabilities in dollars.
        shares_outstanding: Number of fund shares/units outstanding.
        prior_nav_per_share: Prior period NAV per share. None if first period.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Contains nav_per_share, total_nav, variance_from_prior (None if
              no prior provided), variance_pct, total_assets, asset_breakdown,
              status, and timestamp.
    """
    try:
        if shares_outstanding <= 0:
            raise ValueError("shares_outstanding must be positive")
        if liabilities < 0:
            raise ValueError("liabilities cannot be negative")
        if not assets:
            raise ValueError("assets list cannot be empty")

        asset_breakdown: list[dict] = []
        total_assets = 0.0
        for asset in assets:
            if "name" not in asset or "value" not in asset:
                raise ValueError(f"Each asset must have 'name' and 'value'. Got: {asset}")
            val = float(asset["value"])
            total_assets += val
            asset_breakdown.append({"name": asset["name"], "value": round(val, 2)})

        total_nav = total_assets - liabilities
        nav_per_share = total_nav / shares_outstanding

        variance_from_prior: float | None = None
        variance_pct: float | None = None
        if prior_nav_per_share is not None:
            variance_from_prior = nav_per_share - prior_nav_per_share
            if prior_nav_per_share != 0:
                variance_pct = variance_from_prior / prior_nav_per_share
            else:
                variance_pct = None

        result = {
            "nav_per_share": round(nav_per_share, 6),
            "total_nav": round(total_nav, 2),
            "total_assets": round(total_assets, 2),
            "total_liabilities": round(liabilities, 2),
            "shares_outstanding": shares_outstanding,
            "variance_from_prior": round(variance_from_prior, 6) if variance_from_prior is not None else None,
            "variance_pct": round(variance_pct, 6) if variance_pct is not None else None,
            "asset_breakdown": asset_breakdown,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"nav_reconciliation failed: {e}")
        _log_lesson(f"nav_reconciliation: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
