"""Calculate Required Minimum Distribution (RMD) using IRS Uniform Lifetime Table.

MCP Tool Name: required_minimum_distribution_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

# IRS Uniform Lifetime Table (effective 2022+)
_UNIFORM_TABLE: dict[int, float] = {
    72: 27.4, 73: 26.5, 74: 25.5, 75: 24.6, 76: 23.7, 77: 22.9,
    78: 22.0, 79: 21.1, 80: 20.2, 81: 19.4, 82: 18.5, 83: 17.7,
    84: 16.8, 85: 16.0, 86: 15.2, 87: 14.4, 88: 13.7, 89: 12.9,
    90: 12.2, 91: 11.5, 92: 10.8, 93: 10.1, 94: 9.5, 95: 8.9,
    96: 8.4, 97: 7.8, 98: 7.3, 99: 6.8, 100: 6.4, 101: 6.0,
    102: 5.6, 103: 5.2, 104: 4.9, 105: 4.6, 106: 4.3, 107: 4.1,
    108: 3.9, 109: 3.7, 110: 3.5, 111: 3.4, 112: 3.3, 113: 3.1,
    114: 3.0, 115: 2.9, 116: 2.8, 117: 2.7, 118: 2.5, 119: 2.3,
    120: 2.0,
}

TOOL_META: dict[str, Any] = {
    "name": "required_minimum_distribution_calculator",
    "description": "Calculate Required Minimum Distribution (RMD) for traditional IRAs and 401(k)s using the IRS Uniform Lifetime Table. Required starting at age 73 (SECURE 2.0 Act).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "account_balance": {
                "type": "number",
                "description": "Year-end account balance (prior year December 31).",
            },
            "age": {
                "type": "integer",
                "description": "Account holder's age during the distribution year.",
            },
        },
        "required": ["account_balance", "age"],
    },
}


def required_minimum_distribution_calculator(
    account_balance: float,
    age: int,
) -> dict[str, Any]:
    """Calculate Required Minimum Distribution."""
    try:
        if age < 73:
            return {
                "status": "ok",
                "data": {
                    "rmd_required": False,
                    "age": age,
                    "account_balance": account_balance,
                    "note": "Under SECURE 2.0 Act, RMDs begin at age 73 (for those born 1951-1959) "
                    "or age 75 (for those born 1960 or later). No RMD required at your current age.",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        if age > 120:
            age = 120

        distribution_period = _UNIFORM_TABLE.get(age)
        if distribution_period is None:
            return {
                "status": "error",
                "data": {"error": f"Age {age} not found in Uniform Lifetime Table. Valid range: 72-120."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        rmd = account_balance / distribution_period
        rmd_pct = (rmd / account_balance * 100) if account_balance > 0 else 0

        return {
            "status": "ok",
            "data": {
                "rmd_required": True,
                "account_balance": account_balance,
                "age": age,
                "distribution_period": distribution_period,
                "rmd_amount": round(rmd, 2),
                "rmd_percentage": round(rmd_pct, 2),
                "monthly_equivalent": round(rmd / 12, 2),
                "note": "RMD = Account Balance / Distribution Period (Uniform Lifetime Table). "
                "Failure to take full RMD incurs a 25% excise tax on the shortfall (reduced from 50% by SECURE 2.0). "
                "This uses the single-life Uniform Lifetime Table. If your sole beneficiary is a spouse more than 10 years younger, "
                "use the Joint Life Expectancy Table for a lower RMD.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
