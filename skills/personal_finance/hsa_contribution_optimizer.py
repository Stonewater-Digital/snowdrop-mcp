"""Optimize HSA contributions based on coverage type and age.

MCP Tool Name: hsa_contribution_optimizer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "hsa_contribution_optimizer",
    "description": "Calculate optimal HSA contribution limits based on coverage type and age. Shows 2024 limits, catch-up contributions, and tax savings estimates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "coverage_type": {
                "type": "string",
                "description": "Coverage type: 'self' (self-only) or 'family'.",
                "default": "self",
                "enum": ["self", "family"],
            },
            "age": {
                "type": "integer",
                "description": "Account holder's age.",
                "default": 40,
            },
        },
        "required": [],
    },
}

# 2024 HSA limits
_LIMITS_2024 = {
    "self": 4150,
    "family": 8300,
}
_CATCHUP = 1000  # Additional catch-up for age 55+


def hsa_contribution_optimizer(
    coverage_type: str = "self",
    age: int = 40,
) -> dict[str, Any]:
    """Calculate optimal HSA contribution based on coverage type and age."""
    try:
        ct = coverage_type.lower()
        if ct not in _LIMITS_2024:
            return {
                "status": "error",
                "data": {"error": f"Invalid coverage_type '{coverage_type}'. Use 'self' or 'family'."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        base_limit = _LIMITS_2024[ct]
        catch_up_eligible = age >= 55
        catch_up_amount = _CATCHUP if catch_up_eligible else 0
        total_limit = base_limit + catch_up_amount

        # Estimate tax savings at various marginal rates
        tax_scenarios = []
        for rate_label, rate in [("22%", 0.22), ("24%", 0.24), ("32%", 0.32), ("35%", 0.35)]:
            # Income tax savings + FICA savings (7.65%)
            income_tax_savings = total_limit * rate
            fica_savings = total_limit * 0.0765
            total_savings = income_tax_savings + fica_savings
            tax_scenarios.append({
                "marginal_bracket": rate_label,
                "income_tax_savings": round(income_tax_savings, 2),
                "fica_savings": round(fica_savings, 2),
                "total_annual_savings": round(total_savings, 2),
            })

        return {
            "status": "ok",
            "data": {
                "coverage_type": ct,
                "age": age,
                "base_limit_2024": base_limit,
                "catch_up_eligible": catch_up_eligible,
                "catch_up_amount": catch_up_amount,
                "total_contribution_limit": total_limit,
                "monthly_contribution": round(total_limit / 12, 2),
                "per_paycheck_biweekly": round(total_limit / 26, 2),
                "tax_savings_scenarios": tax_scenarios,
                "triple_tax_advantage": [
                    "1. Tax-deductible contributions (reduces taxable income)",
                    "2. Tax-free growth (investments grow without capital gains or dividend taxes)",
                    "3. Tax-free withdrawals for qualified medical expenses",
                ],
                "note": "2024 limits shown. HSAs have no use-it-or-lose-it rule — funds roll over indefinitely. "
                "After age 65, non-medical withdrawals are taxed as ordinary income (like a traditional IRA) but have no penalty. "
                "Catch-up contributions available at age 55+. Must have a qualifying HDHP to contribute.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
