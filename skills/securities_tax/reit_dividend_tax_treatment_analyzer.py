"""REIT dividend tax treatment analyzer.
Breaks dividend into ordinary, capital gain, and return-of-capital buckets.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "reit_dividend_tax_treatment_analyzer",
    "description": "Allocates REIT dividends into tax character categories and rates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "dividend_amount": {"type": "number"},
            "ordinary_pct": {"type": "number"},
            "capital_gain_pct": {"type": "number"},
            "roc_pct": {"type": "number"},
            "ordinary_rate_pct": {"type": "number", "default": 37.0},
            "capital_gain_rate_pct": {"type": "number", "default": 20.0},
        },
        "required": ["dividend_amount", "ordinary_pct", "capital_gain_pct", "roc_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def reit_dividend_tax_treatment_analyzer(
    dividend_amount: float,
    ordinary_pct: float,
    capital_gain_pct: float,
    roc_pct: float,
    ordinary_rate_pct: float = 37.0,
    capital_gain_rate_pct: float = 20.0,
    **_: Any,
) -> dict[str, Any]:
    """Return cash breakdown and tax due per component."""
    try:
        ordinary = dividend_amount * ordinary_pct / 100
        cap_gain = dividend_amount * capital_gain_pct / 100
        roc = dividend_amount * roc_pct / 100
        tax_due = ordinary * ordinary_rate_pct / 100 + cap_gain * capital_gain_rate_pct / 100
        data = {
            "ordinary_income": round(ordinary, 2),
            "capital_gain_component": round(cap_gain, 2),
            "return_of_capital": round(roc, 2),
            "tax_due": round(tax_due, 2),
            "effective_rate_pct": round(tax_due / (dividend_amount - roc) * 100 if dividend_amount > roc else 0.0, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("reit_dividend_tax_treatment_analyzer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
