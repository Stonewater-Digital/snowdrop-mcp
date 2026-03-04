"""
Executive Summary: Resolution planning scorecard aggregating critical functions, inter-affiliate exposures, and TLAC resources.
Inputs: critical_functions (list[dict]), qualified_financial_contracts (int), inter_affiliate_exposures (float), tlac_amount (float)
Outputs: separability_score (float), critical_function_map (list[dict]), resolution_capital_adequacy (float)
MCP Tool Name: resolution_planning_metrics
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "resolution_planning_metrics",
    "description": "Generates key metrics for resolution planning submissions (165(d)).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "critical_functions": {
                "type": "array",
                "description": "Functions with revenue and substitutability inputs.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Function name"},
                        "revenue": {"type": "number", "description": "Annual revenue"},
                        "customers": {"type": "integer", "description": "Customers served"},
                        "substitutability_score": {"type": "number", "description": "1 (easily substitutable) - 5"},
                    },
                    "required": ["name", "revenue", "customers", "substitutability_score"],
                },
            },
            "qualified_financial_contracts": {"type": "integer", "description": "Count of QFCs."},
            "inter_affiliate_exposures": {"type": "number", "description": "Inter-affiliate exposures"},
            "tlac_amount": {"type": "number", "description": "TLAC resources available."},
        },
        "required": ["critical_functions", "qualified_financial_contracts", "inter_affiliate_exposures", "tlac_amount"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Resolution metrics"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def resolution_planning_metrics(
    critical_functions: List[dict[str, Any]],
    qualified_financial_contracts: int,
    inter_affiliate_exposures: float,
    tlac_amount: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        total_revenue = sum(func["revenue"] for func in critical_functions)
        separability = 0.0
        function_map = []
        for func in critical_functions:
            importance = func["revenue"] / total_revenue if total_revenue else 0.0
            substitution_factor = 1 - (func["substitutability_score"] / 5)
            separability += importance * substitution_factor
            function_map.append(
                {
                    "name": func["name"],
                    "importance_pct": round(importance * 100, 2),
                    "substitutability_score": func["substitutability_score"],
                    "customers": func["customers"],
                }
            )
        separability_score = round(separability * 100, 2)
        resolution_capital_adequacy = round(tlac_amount / (inter_affiliate_exposures + 1) * 100, 2)
        data = {
            "separability_score": separability_score,
            "critical_function_map": function_map,
            "qualified_financial_contracts": qualified_financial_contracts,
            "resolution_capital_adequacy_pct": resolution_capital_adequacy,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"resolution_planning_metrics failed: {e}")
        _log_lesson(f"resolution_planning_metrics: {e}")
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
