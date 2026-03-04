"""
Executive Summary: Wrong-way risk adjustment estimating stressed CVA under correlated EAD/PD shocks.
Inputs: counterparty_pd (float), exposure_at_default (float), correlation (float), lgd_pct (float)
Outputs: adjusted_cva (float), wrong_way_multiplier (float), alpha_factor (float)
MCP Tool Name: wrong_way_risk_estimator
"""
import logging
from datetime import datetime, timezone
from statistics import NormalDist
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "wrong_way_risk_estimator",
    "description": "Applies a correlation-driven multiplier to CVA following Basel/WP80 guidance on wrong-way risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "counterparty_pd": {
                "type": "number",
                "description": "Counterparty one-year probability of default (0-1).",
            },
            "exposure_at_default": {
                "type": "number",
                "description": "Exposure at default (EAD) in base currency.",
            },
            "correlation": {
                "type": "number",
                "description": "Correlation between EAD and PD derived from stress testing.",
            },
            "lgd_pct": {
                "type": "number",
                "description": "Loss-given-default percentage (0-100).",
                "default": 60.0,
            },
        },
        "required": ["counterparty_pd", "exposure_at_default", "correlation"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "WWR outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def wrong_way_risk_estimator(
    counterparty_pd: float,
    exposure_at_default: float,
    correlation: float,
    lgd_pct: float = 60.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not 0 < counterparty_pd < 1:
            raise ValueError("counterparty_pd must be between 0 and 1")
        if not -0.99 < correlation < 0.99:
            raise ValueError("correlation must be between -0.99 and 0.99")
        lgd = lgd_pct / 100
        base_cva = counterparty_pd * exposure_at_default * lgd
        z = NormalDist().inv_cdf(0.995)
        dist = NormalDist()
        joint_pd = dist.cdf((NormalDist().inv_cdf(counterparty_pd) + correlation * z) / (1 - correlation**2) ** 0.5)
        adjusted_pd = min(max(joint_pd, counterparty_pd), 1)
        adjusted_cva = adjusted_pd * exposure_at_default * lgd
        multiplier = adjusted_pd / counterparty_pd if counterparty_pd else 1.0
        alpha_factor = correlation / (1 - correlation) if correlation < 0.99 else 1.0

        data = {
            "base_cva": round(base_cva, 2),
            "adjusted_cva": round(adjusted_cva, 2),
            "wrong_way_multiplier": round(multiplier, 4),
            "alpha_factor": round(alpha_factor, 4),
            "adjusted_pd": round(adjusted_pd, 6),
            "tail_z": round(z, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"wrong_way_risk_estimator failed: {e}")
        _log_lesson(f"wrong_way_risk_estimator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
