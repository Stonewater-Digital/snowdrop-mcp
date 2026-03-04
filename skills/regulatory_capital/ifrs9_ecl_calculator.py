"""
Executive Summary: IFRS 9 expected credit loss engine for Stage 1/2/3 exposures using PD term structures.
Inputs: pd_term_structure (list[dict]), lgd_pct (float), ead (float), discount_rate_pct (float), stage (int)
Outputs: twelve_month_ecl (float), lifetime_ecl (float), stage (int), allowance (float)
MCP Tool Name: ifrs9_ecl_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ifrs9_ecl_calculator",
    "description": "Computes 12-month and lifetime ECL discounted at the effective interest rate per IFRS 9.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pd_term_structure": {
                "type": "array",
                "description": "List of PD points with tenor in years (cumulative PD).",
                "items": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "number", "description": "Year index"},
                        "pd": {"type": "number", "description": "Marginal PD for the year"},
                    },
                    "required": ["year", "pd"],
                },
            },
            "lgd_pct": {"type": "number", "description": "Loss given default percentage."},
            "ead": {"type": "number", "description": "Exposure at default."},
            "discount_rate_pct": {"type": "number", "description": "Effective interest rate used for discounting."},
            "stage": {
                "type": "integer",
                "description": "IFRS 9 stage (1,2,3).",
                "enum": [1, 2, 3],
            },
        },
        "required": ["pd_term_structure", "lgd_pct", "ead", "discount_rate_pct", "stage"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "ECL outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _discount_factor(rate_pct: float, year: float) -> float:
    return 1 / ((1 + rate_pct / 100.0) ** year)


def ifrs9_ecl_calculator(
    pd_term_structure: List[Dict[str, float]],
    lgd_pct: float,
    ead: float,
    discount_rate_pct: float,
    stage: int,
    **_: Any,
) -> dict[str, Any]:
    try:
        if stage not in (1, 2, 3):
            raise ValueError("stage must be 1, 2, or 3")
        if not pd_term_structure:
            raise ValueError("pd_term_structure required")
        lgd = lgd_pct / 100.0
        twelve_month_pd = pd_term_structure[0]["pd"] if pd_term_structure else 0.0
        twelve_month_ecl = ead * lgd * twelve_month_pd * _discount_factor(discount_rate_pct, 1)

        lifetime_ecl = 0.0
        survival = 1.0
        pd_term_structure_sorted = sorted(pd_term_structure, key=lambda x: x["year"])
        prev_year = 0.0
        for point in pd_term_structure_sorted:
            year = point["year"]
            delta = max(year - prev_year, 0.0)
            marginal_pd = min(max(point["pd"], 0.0), 1.0)
            hazard = marginal_pd
            default_prob = survival * hazard
            discount = _discount_factor(discount_rate_pct, year)
            lifetime_ecl += ead * lgd * default_prob * discount
            survival *= max(1 - hazard, 0.0)
            prev_year = year

        allowance = twelve_month_ecl if stage == 1 else lifetime_ecl
        data = {
            "twelve_month_ecl": round(twelve_month_ecl, 2),
            "lifetime_ecl": round(lifetime_ecl, 2),
            "stage": stage,
            "allowance": round(allowance, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ifrs9_ecl_calculator failed: {e}")
        _log_lesson(f"ifrs9_ecl_calculator: {e}")
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
