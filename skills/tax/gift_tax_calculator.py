"""Calculate gift tax with annual exclusion and lifetime exemption.

MCP Tool Name: gift_tax_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "gift_tax_calculator",
    "description": "Calculate gift tax liability considering the annual exclusion ($18,000 for 2024), prior gifts, and lifetime exemption ($13.61M for 2024). Tax rate is 40% on amounts exceeding lifetime exemption.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gift_amount": {
                "type": "number",
                "description": "Current gift amount in USD.",
            },
            "prior_year_gifts": {
                "type": "number",
                "description": "Cumulative taxable gifts from prior years (already applied against lifetime exemption) in USD.",
                "default": 0,
            },
            "annual_exclusion": {
                "type": "number",
                "description": "Annual gift tax exclusion amount.",
                "default": 18000,
            },
            "lifetime_exemption": {
                "type": "number",
                "description": "Unified lifetime gift/estate tax exemption.",
                "default": 13610000,
            },
        },
        "required": ["gift_amount"],
    },
}

_TAX_RATE = 0.40  # Top gift tax rate


def gift_tax_calculator(
    gift_amount: float,
    prior_year_gifts: float = 0,
    annual_exclusion: float = 18000,
    lifetime_exemption: float = 13610000,
) -> dict[str, Any]:
    """Calculate gift tax liability."""
    try:
        if gift_amount < 0 or prior_year_gifts < 0:
            return {
                "status": "error",
                "data": {"error": "Amounts must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Amount exceeding annual exclusion is a taxable gift
        taxable_gift = max(gift_amount - annual_exclusion, 0)

        # Cumulative taxable gifts
        cumulative_taxable = prior_year_gifts + taxable_gift

        # Lifetime exemption remaining
        lifetime_used = cumulative_taxable
        lifetime_remaining = max(lifetime_exemption - lifetime_used, 0)

        # Tax owed only if cumulative exceeds lifetime exemption
        amount_over_exemption = max(cumulative_taxable - lifetime_exemption, 0)
        # Tax on prior gifts that were already over
        prior_over = max(prior_year_gifts - lifetime_exemption, 0)
        new_tax = max(amount_over_exemption - prior_over, 0) * _TAX_RATE

        requires_form_709 = taxable_gift > 0

        return {
            "status": "ok",
            "data": {
                "gift_amount": round(gift_amount, 2),
                "annual_exclusion": round(annual_exclusion, 2),
                "taxable_gift": round(taxable_gift, 2),
                "prior_year_taxable_gifts": round(prior_year_gifts, 2),
                "cumulative_taxable_gifts": round(cumulative_taxable, 2),
                "lifetime_exemption": round(lifetime_exemption, 2),
                "lifetime_exemption_used": round(lifetime_used, 2),
                "lifetime_exemption_remaining": round(lifetime_remaining, 2),
                "tax_rate_pct": round(_TAX_RATE * 100, 1),
                "gift_tax_owed": round(new_tax, 2),
                "requires_form_709": requires_form_709,
                "note": "Form 709 must be filed for any gift exceeding the annual exclusion, even if no tax is owed.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
