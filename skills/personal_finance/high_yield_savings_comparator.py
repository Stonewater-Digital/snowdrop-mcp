"""
Executive Smary: Ranks savings accounts by effective yield after fees and balance rules.
Inputs: accounts (list), deposit_amount (float)
Outputs: ranked_accounts (list), effective_annual_rate (float), one_year_projection (list), five_year_projection (list)
MCP Tool Name: high_yield_savings_comparator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "high_yield_savings_comparator",
    "description": (
        "Compares multiple savings accounts by incorporating APY, minimum balances, and "
        "monthly fees to surface the best net yield with 1-year and 5-year projections."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "accounts": {
                "type": "array",
                "description": (
                    "List of account configs with name, apy, min_balance, monthly_fee, "
                    "and fee_waiver_balance."
                ),
                "items": {"type": "object"},
            },
            "deposit_amount": {
                "type": "number",
                "description": "Dollar amount to deposit, must be non-negative.",
            },
        },
        "required": ["accounts", "deposit_amount"],
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


def high_yield_savings_comparator(**kwargs: Any) -> dict:
    """Evaluate savings account options by net yield and projected balances."""
    try:
        accounts = kwargs["accounts"]
        deposit_amount = float(kwargs["deposit_amount"])

        if not isinstance(accounts, list) or not accounts:
            raise ValueError("accounts must be a non-empty list")
        if deposit_amount < 0:
            raise ValueError("deposit_amount must be non-negative")

        ranked = []
        for acct in accounts:
            name = str(acct.get("name", "Unnamed"))
            apy = float(acct.get("apy", 0))
            min_balance = float(acct.get("min_balance", 0))
            monthly_fee = float(acct.get("monthly_fee", 0))
            waiver_balance = float(acct.get("fee_waiver_balance", min_balance))

            if deposit_amount < min_balance:
                effective_rate = 0.0
                fees = monthly_fee * 12
            else:
                fee_applied = 0.0 if deposit_amount >= waiver_balance else monthly_fee * 12
                effective_rate = apy - (fee_applied / max(deposit_amount, 1e-9))
                fees = fee_applied
            one_year_balance = deposit_amount * (1 + effective_rate)
            five_year_balance = deposit_amount * (1 + effective_rate) ** 5
            ranked.append(
                {
                    "name": name,
                    "apy": apy,
                    "effective_yield": effective_rate,
                    "fees_paid": fees,
                    "one_year_balance": one_year_balance,
                    "five_year_balance": five_year_balance,
                }
            )

        ranked.sort(key=lambda x: x["effective_yield"], reverse=True)
        one_year_projection = [
            {"rank": idx + 1, "name": item["name"], "balance": item["one_year_balance"]}
            for idx, item in enumerate(ranked)
        ]
        five_year_projection = [
            {"rank": idx + 1, "name": item["name"], "balance": item["five_year_balance"]}
            for idx, item in enumerate(ranked)
        ]

        return {
            "status": "success",
            "data": {
                "ranked_accounts": ranked,
                "effective_annual_rate": ranked[0]["effective_yield"] if ranked else 0.0,
                "one_year_projection": one_year_projection,
                "five_year_projection": five_year_projection,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"high_yield_savings_comparator failed: {e}")
        _log_lesson(f"high_yield_savings_comparator: {e}")
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
