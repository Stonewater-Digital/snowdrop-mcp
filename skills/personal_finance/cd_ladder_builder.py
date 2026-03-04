"""
Executive Smary: Allocates capital across a CD ladder and estimates blended yield.
Inputs: total_investment (float), cd_terms_available (list), ladder_rungs (int)
Outputs: allocation (list), weighted_average_yield (float), liquidity_schedule (list), total_interest (float)
MCP Tool Name: cd_ladder_builder
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cd_ladder_builder",
    "description": (
        "Constructs a certificate-of-deposit ladder by distributing capital across "
        "available terms, reporting allocation, weighted yield, and liquidity schedule."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_investment": {
                "type": "number",
                "description": "Dollars available to invest, must be positive.",
            },
            "cd_terms_available": {
                "type": "array",
                "description": "List of term options with months and APY values.",
                "items": {"type": "object"},
            },
            "ladder_rungs": {
                "type": "number",
                "description": "Desired number of ladder positions (e.g., 4 for quarterly).",
            },
        },
        "required": ["total_investment", "cd_terms_available", "ladder_rungs"],
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


def cd_ladder_builder(**kwargs: Any) -> dict:
    """Optimize a CD ladder allocation among available terms."""
    try:
        total_investment = float(kwargs["total_investment"])
        terms = kwargs["cd_terms_available"]
        ladder_rungs = int(kwargs["ladder_rungs"])

        if total_investment <= 0:
            raise ValueError("total_investment must be positive")
        if ladder_rungs <= 0:
            raise ValueError("ladder_rungs must be positive")
        if not isinstance(terms, list) or not terms:
            raise ValueError("cd_terms_available must be a non-empty list")

        sorted_terms = sorted(
            (
                {
                    "months": int(item.get("months", 0)),
                    "apy": float(item.get("apy", 0)),
                }
                for item in terms
            ),
            key=lambda x: x["months"],
        )
        sorted_terms = [t for t in sorted_terms if t["months"] > 0 and t["apy"] >= 0]
        if not sorted_terms:
            raise ValueError("cd_terms_available must contain positive months")

        selected_terms = []
        step = max(len(sorted_terms) // ladder_rungs, 1)
        idx = 0
        while len(selected_terms) < ladder_rungs and idx < len(sorted_terms):
            selected_terms.append(sorted_terms[idx])
            idx += step
        while len(selected_terms) < ladder_rungs:
            selected_terms.append(sorted_terms[-1])

        rung_investment = total_investment / ladder_rungs
        allocation = []
        total_interest = 0.0
        weighted_yield = 0.0
        liquidity_schedule = []

        for term in selected_terms:
            months = term["months"]
            apy = term["apy"]
            interest = rung_investment * apy * (months / 12)
            total_interest += interest
            weighted_yield += apy / ladder_rungs
            allocation.append(
                {
                    "months": months,
                    "apy": apy,
                    "amount": rung_investment,
                    "interest": interest,
                }
            )
            liquidity_schedule.append(
                {
                    "month": months,
                    "amount_maturing": rung_investment + interest,
                }
            )

        liquidity_schedule.sort(key=lambda x: x["month"])

        return {
            "status": "success",
            "data": {
                "allocation": allocation,
                "weighted_average_yield": weighted_yield,
                "liquidity_schedule": liquidity_schedule,
                "total_interest": total_interest,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"cd_ladder_builder failed: {e}")
        _log_lesson(f"cd_ladder_builder: {e}")
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
