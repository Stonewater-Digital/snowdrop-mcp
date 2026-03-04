"""
Executive Summary: Tier 2 capital amortization schedule per Basel rules (linear over final 5 years).
Inputs: instrument_notional (float), original_maturity_years (float), remaining_maturity_years (float)
Outputs: eligible_amount (float), amortization_schedule (list[dict]), regulatory_haircut_pct (float)
MCP Tool Name: tier2_instrument_amortization
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "tier2_instrument_amortization",
    "description": "Calculates remaining Tier 2 recognition after applying 20% annual haircuts during final 5 years.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "instrument_notional": {"type": "number", "description": "Current nominal amount."},
            "original_maturity_years": {"type": "number", "description": "Original contractual maturity."},
            "remaining_maturity_years": {"type": "number", "description": "Years left until maturity."},
        },
        "required": ["instrument_notional", "original_maturity_years", "remaining_maturity_years"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Amortization output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def tier2_instrument_amortization(
    instrument_notional: float,
    original_maturity_years: float,
    remaining_maturity_years: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        if remaining_maturity_years > original_maturity_years:
            raise ValueError("remaining maturity cannot exceed original maturity")
        schedule: List[dict[str, Any]] = []
        eligible = instrument_notional
        haircut_pct = 0.0
        if remaining_maturity_years <= 5:
            haircut_pct = (5 - remaining_maturity_years + 1) * 0.2
            haircut_pct = min(max(haircut_pct, 0.0), 1.0)
            eligible = instrument_notional * (1 - haircut_pct)
        for year in range(int(max(remaining_maturity_years - 5, 0)), int(remaining_maturity_years)):
            years_left = remaining_maturity_years - year
            hair = max(0, 1 - max(0, (5 - years_left + 1) * 0.2))
            schedule.append(
                {
                    "years_to_maturity": round(years_left, 2),
                    "eligible_fraction": round(hair, 2),
                }
            )
        data = {
            "eligible_amount": round(eligible, 2),
            "regulatory_haircut_pct": round(haircut_pct * 100, 2),
            "amortization_schedule": schedule,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"tier2_instrument_amortization failed: {e}")
        _log_lesson(f"tier2_instrument_amortization: {e}")
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
