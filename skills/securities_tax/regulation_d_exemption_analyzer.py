"""Regulation D exemption analyzer.
Checks Rule 504/506 thresholds and investor qualifications.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "regulation_d_exemption_analyzer",
    "description": "Determines Reg D rule availability based on size and investor counts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "offering_amount": {"type": "number"},
            "accredited_investors": {"type": "number"},
            "non_accredited_investors": {"type": "number"},
        },
        "required": ["offering_amount", "accredited_investors", "non_accredited_investors"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def regulation_d_exemption_analyzer(
    offering_amount: float,
    accredited_investors: int,
    non_accredited_investors: int,
    **_: Any,
) -> dict[str, Any]:
    """Return eligible rules and disclosure guidance."""
    try:
        rules = []
        if offering_amount <= 10_000_000:
            rules.append("Rule 504")
        if non_accredited_investors <= 35:
            rules.append("Rule 506(b)")
        rules.append("Rule 506(c)")
        disclosure = "enhanced" if non_accredited_investors > 0 else "standard"
        data = {
            "eligible_rules": rules,
            "disclosure_level": disclosure,
            "accredited_ratio_pct": round(accredited_investors / (accredited_investors + non_accredited_investors) * 100 if (accredited_investors + non_accredited_investors) else 0.0, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("regulation_d_exemption_analyzer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
