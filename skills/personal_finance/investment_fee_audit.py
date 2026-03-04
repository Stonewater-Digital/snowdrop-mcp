"""
Executive Smary: Audits investment accounts for advisory and fund fees with long-term impact.
Inputs: accounts (list)
Outputs: total_annual_fees (float), fee_as_pct_of_portfolio (float), 10yr_fee_projection (float), per_account_breakdown (list), fee_reduction_opportunities (list)
MCP Tool Name: investment_fee_audit
"""
import logging
from datetime import datetime, timezone
from typing import Any, List, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "investment_fee_audit",
    "description": (
        "Tallies management, advisory, and transaction fees across accounts and "
        "quantifies the 10-year drag while pointing to expensive providers."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "accounts": {
                "type": "array",
                "description": "List of accounts with provider, balance, expense_ratio, advisory_fee, transaction_fees.",
                "items": {"type": "object"},
            }
        },
        "required": ["accounts"],
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


def investment_fee_audit(**kwargs: Any) -> dict:
    """Aggregate portfolio fees and reveal reduction opportunities."""
    try:
        accounts_input = kwargs["accounts"]
        if not isinstance(accounts_input, list) or not accounts_input:
            raise ValueError("accounts must be a non-empty list")

        total_balance = 0.0
        total_fees = 0.0
        breakdown: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        for account in accounts_input:
            provider = str(account.get("provider", "Unknown"))
            balance = float(account["balance"])
            expense_ratio = float(account.get("expense_ratio", 0.0))
            advisory_fee = float(account.get("advisory_fee", 0.0))
            transaction_fees = float(account.get("transaction_fees", 0.0))
            total_balance += balance
            annual_fee = balance * (expense_ratio + advisory_fee) + transaction_fees
            total_fees += annual_fee
            breakdown.append(
                {
                    "provider": provider,
                    "balance": balance,
                    "expense_ratio": expense_ratio,
                    "advisory_fee": advisory_fee,
                    "transaction_fees": transaction_fees,
                    "annual_fee_dollars": annual_fee,
                }
            )
            if expense_ratio + advisory_fee > 0.01:
                recommendations.append(f"Consider lower-cost alternatives for {provider}.")

        fee_pct = total_fees / total_balance if total_balance > 0 else 0.0
        ten_year_projection = total_fees * 10

        return {
            "status": "success",
            "data": {
                "total_annual_fees": total_fees,
                "fee_as_pct_of_portfolio": fee_pct,
                "10yr_fee_projection": ten_year_projection,
                "per_account_breakdown": breakdown,
                "fee_reduction_opportunities": recommendations,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"investment_fee_audit failed: {e}")
        _log_lesson(f"investment_fee_audit: {e}")
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
