"""Calculate federal income tax using 2024 tax brackets.

MCP Tool Name: tax_bracket_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

# 2024 Federal Income Tax Brackets
_BRACKETS: dict[str, list[tuple[float, float, float]]] = {
    "single": [
        (0, 11600, 0.10),
        (11600, 47150, 0.12),
        (47150, 100525, 0.22),
        (100525, 191950, 0.24),
        (191950, 243725, 0.32),
        (243725, 609350, 0.35),
        (609350, float("inf"), 0.37),
    ],
    "married_jointly": [
        (0, 23200, 0.10),
        (23200, 94300, 0.12),
        (94300, 201050, 0.22),
        (201050, 383900, 0.24),
        (383900, 487450, 0.32),
        (487450, 731200, 0.35),
        (731200, float("inf"), 0.37),
    ],
    "married_separately": [
        (0, 11600, 0.10),
        (11600, 47150, 0.12),
        (47150, 100525, 0.22),
        (100525, 191950, 0.24),
        (191950, 243725, 0.32),
        (243725, 365600, 0.35),
        (365600, float("inf"), 0.37),
    ],
    "head_of_household": [
        (0, 16550, 0.10),
        (16550, 63100, 0.12),
        (63100, 100500, 0.22),
        (100500, 191950, 0.24),
        (191950, 243700, 0.32),
        (243700, 609350, 0.35),
        (609350, float("inf"), 0.37),
    ],
}

TOOL_META: dict[str, Any] = {
    "name": "tax_bracket_calculator",
    "description": "Calculate federal income tax owed using 2024 tax brackets. Shows marginal rate, effective rate, and tax owed per bracket.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "taxable_income": {
                "type": "number",
                "description": "Taxable income (after deductions).",
            },
            "filing_status": {
                "type": "string",
                "description": "Filing status.",
                "default": "single",
                "enum": ["single", "married_jointly", "married_separately", "head_of_household"],
            },
        },
        "required": ["taxable_income"],
    },
}


def tax_bracket_calculator(
    taxable_income: float,
    filing_status: str = "single",
) -> dict[str, Any]:
    """Calculate federal income tax using 2024 tax brackets."""
    try:
        status = filing_status.lower().replace(" ", "_").replace("-", "_")
        if status not in _BRACKETS:
            return {
                "status": "error",
                "data": {"error": f"Invalid filing_status '{filing_status}'. Use: single, married_jointly, married_separately, head_of_household."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        brackets = _BRACKETS[status]
        total_tax = 0.0
        marginal_rate = 0.0
        bracket_breakdown: list[dict[str, Any]] = []

        for lower, upper, rate in brackets:
            if taxable_income <= lower:
                break

            bracket_income = min(taxable_income, upper) - lower
            bracket_tax = bracket_income * rate
            total_tax += bracket_tax
            marginal_rate = rate

            bracket_breakdown.append({
                "bracket": f"{rate*100:.0f}%",
                "range": f"${lower:,.0f} - ${upper:,.0f}" if upper != float("inf") else f"${lower:,.0f}+",
                "taxable_in_bracket": round(bracket_income, 2),
                "tax_in_bracket": round(bracket_tax, 2),
            })

        effective_rate = (total_tax / taxable_income * 100) if taxable_income > 0 else 0

        return {
            "status": "ok",
            "data": {
                "taxable_income": taxable_income,
                "filing_status": status,
                "total_tax_owed": round(total_tax, 2),
                "marginal_rate_pct": round(marginal_rate * 100, 0),
                "effective_rate_pct": round(effective_rate, 2),
                "bracket_breakdown": bracket_breakdown,
                "after_tax_income": round(taxable_income - total_tax, 2),
                "note": "2024 federal income tax brackets. This is federal tax only — does not include state, "
                "local, FICA, or other taxes. Taxable income = AGI minus deductions (standard or itemized). "
                "2024 standard deduction: $14,600 (single), $29,200 (married filing jointly).",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
