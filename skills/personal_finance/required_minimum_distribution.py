"""
Executive Smary: Calculates required minimum distributions using IRS life expectancy factors.
Inputs: account_balance (float), owner_age (int), account_type (str)
Outputs: rmd_amount (float), distribution_period (float), effective_rate (float), next_5yr_schedule (list)
MCP Tool Name: required_minimum_distribution
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

UNIFORM_LIFETIME_FACTORS = {
    72: 27.4,
    73: 26.5,
    74: 25.5,
    75: 24.7,
    76: 23.8,
    77: 22.9,
    78: 22.0,
    79: 21.1,
    80: 20.2,
    81: 19.4,
    82: 18.5,
    83: 17.7,
    84: 16.8,
    85: 16.0,
    86: 15.2,
    87: 14.4,
    88: 13.7,
    89: 12.9,
    90: 12.2,
    91: 11.5,
    92: 10.8,
    93: 10.1,
    94: 9.5,
    95: 8.9,
    96: 8.4,
    97: 7.8,
    98: 7.3,
    99: 6.8,
    100: 6.4,
    101: 6.0,
    102: 5.6,
    103: 5.2,
    104: 4.9,
    105: 4.6,
    106: 4.3,
    107: 4.1,
    108: 3.9,
    109: 3.7,
    110: 3.5,
    111: 3.4,
    112: 3.3,
    113: 3.1,
    114: 3.0,
    115: 2.9,
}


def _factor_for_age(age: int, account_type: str) -> float:
    if account_type == "inherited":
        return max(1.0, 40 - 0.9 * max(age - 30, 0))
    if account_type == "traditional_ira" and age < 72:
        return 29.1
    if age in UNIFORM_LIFETIME_FACTORS:
        return UNIFORM_LIFETIME_FACTORS[age]
    if age < 72:
        return 29.1
    last_age = max(UNIFORM_LIFETIME_FACTORS)
    last_factor = UNIFORM_LIFETIME_FACTORS[last_age]
    decay = 0.1 * (age - last_age)
    return max(last_factor - decay, 1.0)


TOOL_META = {
    "name": "required_minimum_distribution",
    "description": (
        "Applies IRS life expectancy divisors to compute required minimum distributions "
        "for traditional IRAs, 401(k)s, and inherited accounts while projecting 5 years ahead."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "account_balance": {
                "type": "number",
                "description": "Balance subject to RMD calculations, must be positive.",
            },
            "owner_age": {
                "type": "number",
                "description": "Owner age at year end, determines life expectancy factor.",
            },
            "account_type": {
                "type": "string",
                "description": "traditional_ira, 401k, or inherited.",
            },
        },
        "required": ["account_balance", "owner_age", "account_type"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def required_minimum_distribution(**kwargs: Any) -> dict:
    """Compute required minimum distribution and a forward-looking schedule."""
    try:
        balance = float(kwargs["account_balance"])
        owner_age = int(kwargs["owner_age"])
        account_type = str(kwargs["account_type"]).strip().lower()

        if balance <= 0:
            raise ValueError("account_balance must be positive")
        if owner_age <= 0:
            raise ValueError("owner_age must be positive")
        if account_type not in {"traditional_ira", "401k", "inherited"}:
            raise ValueError("account_type must be traditional_ira, 401k, or inherited")

        factor = _factor_for_age(owner_age, account_type)
        rmd_amount = balance / factor
        schedule = []
        projected_balance = balance
        for i in range(5):
            age = owner_age + i
            factor_i = _factor_for_age(age, account_type)
            rmd = projected_balance / factor_i
            projected_balance = max(projected_balance - rmd, 0.0)
            schedule.append(
                {
                    "age": age,
                    "factor": factor_i,
                    "rmd_amount": rmd,
                    "ending_balance": projected_balance,
                }
            )

        return {
            "status": "success",
            "data": {
                "rmd_amount": rmd_amount,
                "distribution_period": factor,
                "effective_rate": rmd_amount / balance,
                "next_5yr_schedule": schedule,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"required_minimum_distribution failed: {e}")
        _log_lesson(f"required_minimum_distribution: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
