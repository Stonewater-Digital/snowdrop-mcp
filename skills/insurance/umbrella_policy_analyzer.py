"""Analyze umbrella insurance needs based on total assets and existing liability coverage.

MCP Tool Name: umbrella_policy_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "umbrella_policy_analyzer",
    "description": "Analyze umbrella insurance needs: recommended coverage based on total assets minus existing liability coverage, with premium estimate.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_assets": {"type": "number", "description": "Total net worth / assets to protect."},
            "existing_auto_liability": {"type": "number", "description": "Existing auto liability coverage limit."},
            "existing_home_liability": {"type": "number", "description": "Existing homeowners liability coverage limit."},
        },
        "required": ["total_assets", "existing_auto_liability", "existing_home_liability"],
    },
}


def umbrella_policy_analyzer(
    total_assets: float,
    existing_auto_liability: float,
    existing_home_liability: float,
) -> dict[str, Any]:
    """Analyze umbrella insurance needs."""
    try:
        existing_total = existing_auto_liability + existing_home_liability
        gap = total_assets - existing_total
        # Recommend at least $1M or enough to cover assets
        recommended = max(gap, 1_000_000)
        # Round up to nearest million
        recommended = ((recommended // 1_000_000) + 1) * 1_000_000 if recommended % 1_000_000 != 0 else recommended

        # Premium estimate: ~$150-300 per $1M
        premium_per_million = 200
        estimated_annual_premium = (recommended / 1_000_000) * premium_per_million

        return {
            "status": "ok",
            "data": {
                "total_assets": total_assets,
                "existing_auto_liability": existing_auto_liability,
                "existing_home_liability": existing_home_liability,
                "existing_total_liability": existing_total,
                "coverage_gap": round(gap, 2),
                "recommended_umbrella": round(recommended, 2),
                "estimated_annual_premium": round(estimated_annual_premium, 2),
                "estimated_monthly_premium": round(estimated_annual_premium / 12, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
