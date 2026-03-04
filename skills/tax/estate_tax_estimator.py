"""Estimate federal estate tax liability.

MCP Tool Name: estate_tax_estimator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "estate_tax_estimator",
    "description": "Estimate federal estate tax at 40% rate on taxable estate exceeding the exemption ($13.61M for 2024) after deductions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_estate": {
                "type": "number",
                "description": "Gross estate value in USD (total assets at death).",
            },
            "deductions": {
                "type": "number",
                "description": "Total deductions (marital, charitable, debts, expenses) in USD.",
                "default": 0,
            },
            "exemption": {
                "type": "number",
                "description": "Estate tax exemption amount.",
                "default": 13610000,
            },
        },
        "required": ["gross_estate"],
    },
}

_ESTATE_TAX_RATE = 0.40


def estate_tax_estimator(
    gross_estate: float,
    deductions: float = 0,
    exemption: float = 13610000,
) -> dict[str, Any]:
    """Estimate federal estate tax."""
    try:
        if gross_estate < 0 or deductions < 0:
            return {
                "status": "error",
                "data": {"error": "Amounts must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        net_estate = max(gross_estate - deductions, 0)
        taxable_estate = max(net_estate - exemption, 0)
        estate_tax = taxable_estate * _ESTATE_TAX_RATE
        effective_rate = (estate_tax / gross_estate * 100) if gross_estate > 0 else 0.0

        filing_required = gross_estate > exemption

        return {
            "status": "ok",
            "data": {
                "gross_estate": round(gross_estate, 2),
                "deductions": round(deductions, 2),
                "net_estate": round(net_estate, 2),
                "exemption": round(exemption, 2),
                "taxable_estate": round(taxable_estate, 2),
                "tax_rate_pct": round(_ESTATE_TAX_RATE * 100, 1),
                "estimated_estate_tax": round(estate_tax, 2),
                "effective_rate_pct": round(effective_rate, 2),
                "estate_after_tax": round(net_estate - estate_tax, 2),
                "filing_required": filing_required,
                "note": "Form 706 required if gross estate exceeds exemption. Portability election available for married couples.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
