"""
Executive Summary: CET1 deduction engine applying Basel threshold rules for goodwill, DTAs, and MSRs.
Inputs: goodwill (float), deferred_tax_assets (float), mortgage_servicing_rights (float), significant_investments (float), threshold_limits (dict), cet1_before_deductions (float)
Outputs: total_deductions (float), cet1_after_deductions (float), threshold_utilization (dict)
MCP Tool Name: cet1_deduction_engine
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cet1_deduction_engine",
    "description": "Computes CET1 deductions with 15% aggregate threshold for DTAs, MSRs, and investments.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "goodwill": {"type": "number", "description": "Goodwill net of deferred tax liabilities."},
            "deferred_tax_assets": {"type": "number", "description": "DTAs arising from temporary differences."},
            "mortgage_servicing_rights": {"type": "number", "description": "MSRs amount."},
            "significant_investments": {"type": "number", "description": "Significant investments in financial sector entities."},
            "cet1_before_deductions": {"type": "number", "description": "CET1 before regulatory deductions."},
            "threshold_limits": {
                "type": "object",
                "description": "Threshold percentages (e.g., 10%, 15%).",
                "properties": {
                    "individual_threshold_pct": {"type": "number", "description": "Individual threshold, default 10%", "default": 10.0},
                    "aggregate_threshold_pct": {"type": "number", "description": "Aggregate threshold, default 15%", "default": 15.0},
                },
            },
        },
        "required": [
            "goodwill",
            "deferred_tax_assets",
            "mortgage_servicing_rights",
            "significant_investments",
            "cet1_before_deductions",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Deduction details"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def cet1_deduction_engine(
    goodwill: float,
    deferred_tax_assets: float,
    mortgage_servicing_rights: float,
    significant_investments: float,
    cet1_before_deductions: float,
    threshold_limits: Dict[str, float] | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        thresholds = {"individual_threshold_pct": 10.0, "aggregate_threshold_pct": 15.0}
        if threshold_limits:
            thresholds.update(threshold_limits)
        individual_limit = cet1_before_deductions * thresholds["individual_threshold_pct"] / 100.0
        aggregate_limit = cet1_before_deductions * thresholds["aggregate_threshold_pct"] / 100.0
        limited_assets = [
            ("dtas", deferred_tax_assets),
            ("msrs", mortgage_servicing_rights),
            ("investments", significant_investments),
        ]
        individual_deductions = {name: max(amount - individual_limit, 0.0) for name, amount in limited_assets}
        residuals = {name: amount - individual_deductions[name] for name, amount in limited_assets}
        aggregate_excess = max(sum(residuals.values()) - aggregate_limit, 0.0)
        aggregate_allocation = aggregate_excess / len(residuals) if residuals else 0.0
        aggregate_deductions = {name: min(residuals[name], aggregate_allocation) for name in residuals}
        total_deductions = goodwill + sum(individual_deductions.values()) + sum(aggregate_deductions.values())
        cet1_after = max(cet1_before_deductions - total_deductions, 0.0)
        data = {
            "total_deductions": round(total_deductions, 2),
            "cet1_after_deductions": round(cet1_after, 2),
            "threshold_utilization": {
                "individual_limit": round(individual_limit, 2),
                "aggregate_limit": round(aggregate_limit, 2),
                "aggregate_excess": round(aggregate_excess, 2),
            },
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"cet1_deduction_engine failed: {e}")
        _log_lesson(f"cet1_deduction_engine: {e}")
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
