"""
Executive Smary: Runs sensitivity on CAC, LTV, margin, and churn to stress unit economics.
Inputs: base_cac (float), base_ltv (float), base_margin (float), base_churn (float), variation_pct (float)
Outputs: sensitivity_table (list), worst_case (dict), best_case (dict), breakeven_scenarios (list)
MCP Tool Name: unit_economics_sensitivity
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "unit_economics_sensitivity",
    "description": (
        "Applies +/- variation to CAC, LTV, margin, and churn to highlight best/worst "
        "case unit economics and breakeven thresholds."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "base_cac": {
                "type": "number",
                "description": "Baseline customer acquisition cost.",
            },
            "base_ltv": {
                "type": "number",
                "description": "Baseline lifetime value per customer.",
            },
            "base_margin": {
                "type": "number",
                "description": "Gross margin percentage as decimal.",
            },
            "base_churn": {
                "type": "number",
                "description": "Churn rate as decimal.",
            },
            "variation_pct": {
                "type": "number",
                "description": "Sensitivity swing percentage (e.g., 0.2 for +/-20%).",
            },
        },
        "required": ["base_cac", "base_ltv", "base_margin", "base_churn", "variation_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def unit_economics_sensitivity(**kwargs: Any) -> dict:
    """Produce sensitivity cases for key unit economics inputs."""
    try:
        base_cac = float(kwargs["base_cac"])
        base_ltv = float(kwargs["base_ltv"])
        base_margin = float(kwargs["base_margin"])
        base_churn = float(kwargs["base_churn"])
        variation_pct = float(kwargs["variation_pct"])

        scenarios = []
        best_case = None
        worst_case = None
        breakeven = []

        for delta in (-variation_pct, 0, variation_pct):
            cac = base_cac * (1 + delta)
            ltv = base_ltv * (1 - delta)
            margin = max(min(base_margin * (1 + delta), 1.0), 0.0)
            churn = max(base_churn * (1 + delta), 0.0)
            ratio = ltv / cac if cac > 0 else float("inf")
            scenario = {"delta": delta, "cac": cac, "ltv": ltv, "margin": margin, "churn": churn, "ltv_cac": ratio}
            scenarios.append(scenario)
            if best_case is None or ratio > best_case["ltv_cac"]:
                best_case = scenario
            if worst_case is None or ratio < worst_case["ltv_cac"]:
                worst_case = scenario
            if abs(ratio - 1) <= 0.1:
                breakeven.append(scenario)

        return {
            "status": "success",
            "data": {
                "sensitivity_table": scenarios,
                "worst_case": worst_case,
                "best_case": best_case,
                "breakeven_scenarios": breakeven,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"unit_economics_sensitivity failed: {e}")
        _log_lesson(f"unit_economics_sensitivity: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
