"""Investor qualification validator.
Checks net worth, income, and sophistication to qualify investors.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "investor_qualification_validator",
    "description": "Validates accredited investor status using income and net worth thresholds.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_worth": {"type": "number"},
            "annual_income": {"type": "number"},
            "joint": {"type": "boolean", "default": False},
            "professional_certifications": {"type": "boolean", "default": False},
        },
        "required": ["net_worth", "annual_income"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def investor_qualification_validator(
    net_worth: float,
    annual_income: float,
    joint: bool = False,
    professional_certifications: bool = False,
    **_: Any,
) -> dict[str, Any]:
    """Return accreditation decision and qualifying path."""
    try:
        income_threshold = 300_000 if joint else 200_000
        net_worth_threshold = 1_000_000
        qualifies = (
            net_worth > net_worth_threshold
            or annual_income > income_threshold
            or professional_certifications
        )
        reason = "net_worth" if net_worth > net_worth_threshold else "income" if annual_income > income_threshold else "certification" if professional_certifications else "none"
        data = {
            "accredited": qualifies,
            "qualification_path": reason,
            "income_threshold": income_threshold,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("investor_qualification_validator failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
