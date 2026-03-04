"""
Execuve Summary: Compares EV/EBITDA across companies and evaluates relative valuation.
Inputs: companies (list[dict])
Outputs: ev_ebitda_per_company (dict), sector_median (float), relative_valuation (dict), peg_adjusted_ev_ebitda (dict)
MCP Tool Name: ev_ebitda_comparator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ev_ebitda_comparator",
    "description": "Computes EV/EBITDA multiples per company, sector median, and growth-adjusted comparisons.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "companies": {"type": "array", "description": "List of {name, ev, ebitda, growth_rate} objects."}
        },
        "required": ["companies"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def ev_ebitda_comparator(**kwargs: Any) -> dict:
    """Generates EV/EBITDA comps and labels companies as cheap/fair/expensive."""
    try:
        companies = kwargs.get("companies")
        if not isinstance(companies, list) or len(companies) == 0:
            raise ValueError("companies must be non-empty list")

        multiples = {}
        peg_adjusted = {}
        for entry in companies:
            if not isinstance(entry, dict):
                raise ValueError("each company must be a dict")
            name = entry.get("name")
            ev = entry.get("ev")
            ebitda = entry.get("ebitda")
            growth = entry.get("growth_rate", 0)
            if not name or not isinstance(ev, (int, float)) or not isinstance(ebitda, (int, float)):
                raise ValueError("company entries must include name, ev, ebitda")
            multiple = ev / ebitda if ebitda else math.inf
            multiples[name] = multiple
            peg_adjusted[name] = multiple / (growth if isinstance(growth, (int, float)) and growth > 0 else 1)

        sorted_multiples = sorted(multiples.values())
        mid = len(sorted_multiples) // 2
        sector_median = sorted_multiples[mid] if len(sorted_multiples) % 2 else (
            sorted_multiples[mid - 1] + sorted_multiples[mid]) / 2

        relative = {}
        for name, multiple in multiples.items():
            if multiple < sector_median * 0.9:
                relative[name] = "cheap"
            elif multiple > sector_median * 1.1:
                relative[name] = "expensive"
            else:
                relative[name] = "fair"

        return {
            "status": "success",
            "data": {
                "ev_ebitda_per_company": multiples,
                "sector_median": sector_median,
                "relative_valuation": relative,
                "peg_adjusted_ev_ebitda": peg_adjusted
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ev_ebitda_comparator failed: {e}")
        _log_lesson(f"ev_ebitda_comparator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
