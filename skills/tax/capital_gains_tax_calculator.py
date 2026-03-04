"""Calculate capital gains tax including short-term vs long-term rates and NIIT.

MCP Tool Name: capital_gains_tax_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "capital_gains_tax_calculator",
    "description": "Calculate capital gains tax with short-term vs long-term classification, 0/15/20% rates based on income bracket, and 3.8% NIIT when applicable.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "purchase_price": {
                "type": "number",
                "description": "Original purchase price (cost basis) in USD.",
            },
            "sale_price": {
                "type": "number",
                "description": "Sale price in USD.",
            },
            "holding_period_months": {
                "type": "number",
                "description": "Number of months the asset was held.",
            },
            "income_bracket": {
                "type": "string",
                "description": "Income bracket: low, middle, or high. Determines long-term CG rate (0%, 15%, 20%) and NIIT applicability.",
                "enum": ["low", "middle", "high"],
                "default": "middle",
            },
        },
        "required": ["purchase_price", "sale_price", "holding_period_months"],
    },
}

# 2024 long-term capital gains rate thresholds (single filer reference)
_LTCG_RATES = {
    "low": 0.00,      # 0% rate: taxable income up to ~$47,025 single
    "middle": 0.15,    # 15% rate: up to ~$518,900 single
    "high": 0.20,      # 20% rate: above ~$518,900 single
}

_NIIT_RATE = 0.038  # Net Investment Income Tax
_NIIT_THRESHOLD_SINGLE = 200_000  # Applies to high bracket


def capital_gains_tax_calculator(
    purchase_price: float,
    sale_price: float,
    holding_period_months: float,
    income_bracket: str = "middle",
) -> dict[str, Any]:
    """Calculate capital gains tax with short/long-term classification and NIIT."""
    try:
        income_bracket = income_bracket.lower().strip()
        if income_bracket not in _LTCG_RATES:
            return {
                "status": "error",
                "data": {"error": f"Invalid income_bracket '{income_bracket}'. Must be low, middle, or high."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        gain = sale_price - purchase_price
        is_gain = gain > 0
        is_long_term = holding_period_months > 12

        if not is_gain:
            # Capital loss
            return {
                "status": "ok",
                "data": {
                    "purchase_price": round(purchase_price, 2),
                    "sale_price": round(sale_price, 2),
                    "gain_loss": round(gain, 2),
                    "classification": "capital_loss",
                    "holding_period_months": holding_period_months,
                    "tax_owed": 0.0,
                    "note": "Capital losses can offset gains. Up to $3,000 in net losses can offset ordinary income per year. Excess carries forward.",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        if is_long_term:
            rate = _LTCG_RATES[income_bracket]
            classification = "long_term"
        else:
            # Short-term gains taxed as ordinary income; approximate by bracket
            ordinary_rates = {"low": 0.12, "middle": 0.22, "high": 0.37}
            rate = ordinary_rates[income_bracket]
            classification = "short_term"

        base_tax = gain * rate

        # NIIT applies to high-income taxpayers
        niit_applies = income_bracket == "high"
        niit_amount = gain * _NIIT_RATE if niit_applies else 0.0
        total_tax = base_tax + niit_amount

        return {
            "status": "ok",
            "data": {
                "purchase_price": round(purchase_price, 2),
                "sale_price": round(sale_price, 2),
                "capital_gain": round(gain, 2),
                "classification": classification,
                "holding_period_months": holding_period_months,
                "tax_rate_pct": round(rate * 100, 2),
                "base_tax": round(base_tax, 2),
                "niit_applies": niit_applies,
                "niit_amount": round(niit_amount, 2),
                "total_tax": round(total_tax, 2),
                "after_tax_proceeds": round(sale_price - total_tax, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
