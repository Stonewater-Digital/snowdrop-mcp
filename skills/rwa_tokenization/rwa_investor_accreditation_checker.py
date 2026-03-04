"""Check whether an investor meets accreditation criteria for RWAs.
Supports US-style income/net-worth thresholds."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_investor_accreditation_checker",
    "description": "Evaluates investor profile against configurable accreditation thresholds.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "annual_income": {"type": "number", "description": "Investor annual income"},
            "net_worth": {"type": "number", "description": "Investor net worth"},
            "min_income_threshold": {"type": "number", "description": "Income threshold", "default": 200000},
            "min_net_worth_threshold": {"type": "number", "description": "Net worth threshold", "default": 1000000},
        },
        "required": ["annual_income", "net_worth"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def rwa_investor_accreditation_checker(
    annual_income: float,
    net_worth: float,
    min_income_threshold: float = 200_000.0,
    min_net_worth_threshold: float = 1_000_000.0,
    **_: Any,
) -> dict[str, Any]:
    """Evaluate accreditation status.

    Args:
        annual_income: Investor annual income.
        net_worth: Investor net worth.
        min_income_threshold: Minimum income requirement.
        min_net_worth_threshold: Minimum net worth requirement.

    Returns:
        Dict indicating accreditation result and shortfall gap.
    """
    try:
        income_ok = annual_income >= min_income_threshold
        net_worth_ok = net_worth >= min_net_worth_threshold
        accredited = income_ok or net_worth_ok
        data = {
            "accredited": accredited,
            "income_gap": round(max(min_income_threshold - annual_income, 0), 2),
            "net_worth_gap": round(max(min_net_worth_threshold - net_worth, 0), 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_investor_accreditation_checker failure: %s", exc)
        log_lesson(f"rwa_investor_accreditation_checker: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
