"""Calculate employer-side payroll taxes (FICA, FUTA, SUTA).

MCP Tool Name: employer_tax_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "employer_tax_calculator",
    "description": "Calculate employer-side payroll taxes: employer FICA match (7.65%), FUTA (0.6% on first $7,000), and SUTA (variable on wage base).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_payroll": {
                "type": "number",
                "description": "Total gross payroll for the period in USD.",
            },
            "num_employees": {
                "type": "integer",
                "description": "Number of employees on payroll.",
            },
            "futa_rate": {
                "type": "number",
                "description": "FUTA tax rate as a decimal (after state credit, typically 0.006).",
                "default": 0.006,
            },
            "suta_rate": {
                "type": "number",
                "description": "SUTA (state unemployment) tax rate as a decimal.",
                "default": 0.027,
            },
        },
        "required": ["gross_payroll", "num_employees"],
    },
}

_FICA_EMPLOYER_RATE = 0.0765
_SS_WAGE_BASE = 168600  # 2024 Social Security wage base
_FUTA_WAGE_BASE = 7000
_SUTA_WAGE_BASE = 7000  # Varies by state; using federal minimum


def employer_tax_calculator(
    gross_payroll: float,
    num_employees: int,
    futa_rate: float = 0.006,
    suta_rate: float = 0.027,
) -> dict[str, Any]:
    """Calculate employer payroll taxes."""
    try:
        if gross_payroll < 0 or num_employees <= 0:
            return {
                "status": "error",
                "data": {"error": "gross_payroll must be non-negative and num_employees must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Employer FICA match
        fica_employer = gross_payroll * _FICA_EMPLOYER_RATE

        # FICA breakdown
        avg_wage = gross_payroll / num_employees
        ss_taxable_per_employee = min(avg_wage, _SS_WAGE_BASE)
        ss_employer = ss_taxable_per_employee * 0.062 * num_employees
        medicare_employer = gross_payroll * 0.0145

        # FUTA: applies on first $7,000 per employee per year
        futa_taxable_per_employee = min(avg_wage, _FUTA_WAGE_BASE)
        futa_total = futa_taxable_per_employee * futa_rate * num_employees

        # SUTA: similar structure
        suta_taxable_per_employee = min(avg_wage, _SUTA_WAGE_BASE)
        suta_total = suta_taxable_per_employee * suta_rate * num_employees

        total_employer_tax = fica_employer + futa_total + suta_total
        cost_per_employee = total_employer_tax / num_employees if num_employees > 0 else 0
        tax_as_pct_of_payroll = (total_employer_tax / gross_payroll * 100) if gross_payroll > 0 else 0

        return {
            "status": "ok",
            "data": {
                "gross_payroll": round(gross_payroll, 2),
                "num_employees": num_employees,
                "avg_wage_per_employee": round(avg_wage, 2),
                "employer_fica": {
                    "social_security": round(ss_employer, 2),
                    "medicare": round(medicare_employer, 2),
                    "total": round(fica_employer, 2),
                },
                "futa": {
                    "rate_pct": round(futa_rate * 100, 3),
                    "wage_base": _FUTA_WAGE_BASE,
                    "total": round(futa_total, 2),
                },
                "suta": {
                    "rate_pct": round(suta_rate * 100, 3),
                    "wage_base": _SUTA_WAGE_BASE,
                    "total": round(suta_total, 2),
                },
                "total_employer_tax": round(total_employer_tax, 2),
                "cost_per_employee": round(cost_per_employee, 2),
                "tax_as_pct_of_payroll": round(tax_as_pct_of_payroll, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
