"""
Executive Summary: Automated DRIP execution — computes REIT dividend reinvestment shares, fractional handling, and new cost basis.
Inputs: dividend (dict: amount_usd float, ex_date str, payment_date str, share_price float)
Outputs: shares_purchased (float), fractional_shares (float), new_cost_basis_per_share (float), reinvestment_summary (dict)
MCP Tool Name: reit_dividend_reinvestment_logic
"""
import os
import logging
import math
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "reit_dividend_reinvestment_logic",
    "description": (
        "Executes Dividend Reinvestment Plan (DRIP) logic for a REIT distribution. "
        "Calculates whole and fractional shares purchasable at the current share price, "
        "computes the blended new cost basis per share, and produces a reinvestment "
        "summary suitable for ledger entry."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "dividend": {
                "type": "object",
                "properties": {
                    "amount_usd":    {"type": "number", "description": "Gross dividend amount in USD."},
                    "ex_date":       {"type": "string", "description": "Ex-dividend date (ISO 8601)."},
                    "payment_date":  {"type": "string", "description": "Dividend payment date (ISO 8601)."},
                    "share_price":   {"type": "number", "description": "Share price at reinvestment."},
                    "existing_shares": {"type": "number", "default": 0, "description": "Shares held before reinvestment."},
                    "existing_cost_basis": {"type": "number", "default": 0.0, "description": "Total cost basis of existing shares (USD)."},
                },
                "required": ["amount_usd", "ex_date", "payment_date", "share_price"],
            }
        },
        "required": ["dividend"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "shares_purchased":         {"type": "number"},
            "fractional_shares":        {"type": "number"},
            "new_cost_basis_per_share": {"type": "number"},
            "reinvestment_summary":     {"type": "object"},
            "status":                   {"type": "string"},
            "timestamp":                {"type": "string"},
        },
        "required": [
            "shares_purchased", "fractional_shares", "new_cost_basis_per_share",
            "reinvestment_summary", "status", "timestamp"
        ],
    },
}


def reit_dividend_reinvestment_logic(dividend: dict[str, Any]) -> dict[str, Any]:
    """Execute DRIP calculations for a REIT dividend distribution.

    Whole shares are purchased at the given share_price. Any remainder dollar
    amount (less than one full share) is treated as fractional shares and included
    in the position. The blended new cost basis per share is recalculated over the
    combined position (existing + newly purchased).

    Args:
        dividend: REIT dividend descriptor with keys:
            - amount_usd (float): Gross dividend amount to reinvest.
            - ex_date (str): Ex-dividend date in ISO 8601 format.
            - payment_date (str): Payment/settlement date in ISO 8601 format.
            - share_price (float): Price per share at time of reinvestment.
            - existing_shares (float, optional): Shares owned before DRIP. Default 0.
            - existing_cost_basis (float, optional): Total cost basis of existing
              shares in USD. Default 0.0.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - shares_purchased (float): Total new shares acquired (whole + fractional).
            - fractional_shares (float): Sub-share portion of the purchase.
            - new_cost_basis_per_share (float): Blended cost basis per share post-DRIP.
            - reinvestment_summary (dict): Full ledger-ready summary.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        amount_usd: float = float(dividend.get("amount_usd", 0.0))
        ex_date: str = str(dividend.get("ex_date", ""))
        payment_date: str = str(dividend.get("payment_date", ""))
        share_price: float = float(dividend.get("share_price", 0.0))
        existing_shares: float = float(dividend.get("existing_shares", 0.0))
        existing_cost_basis: float = float(dividend.get("existing_cost_basis", 0.0))

        if share_price <= 0:
            raise ValueError("share_price must be greater than zero.")
        if amount_usd < 0:
            raise ValueError("amount_usd cannot be negative.")

        # Compute shares purchasable
        raw_shares: float = amount_usd / share_price
        whole_shares: float = math.floor(raw_shares)
        fractional_shares: float = round(raw_shares - whole_shares, 8)
        total_shares_purchased: float = round(raw_shares, 8)  # whole + fractional

        # Cost of reinvestment
        cost_of_reinvestment: float = round(amount_usd, 2)

        # Blended cost basis
        total_shares_after: float = existing_shares + total_shares_purchased
        total_cost_basis_after: float = existing_cost_basis + cost_of_reinvestment

        new_cost_basis_per_share: float = (
            round(total_cost_basis_after / total_shares_after, 6)
            if total_shares_after > 0
            else share_price
        )

        reinvestment_summary: dict[str, Any] = {
            "ex_date":                  ex_date,
            "payment_date":             payment_date,
            "dividend_amount_usd":      amount_usd,
            "reinvestment_price":       share_price,
            "whole_shares_purchased":   whole_shares,
            "fractional_shares":        fractional_shares,
            "total_shares_purchased":   total_shares_purchased,
            "cost_of_reinvestment_usd": cost_of_reinvestment,
            "existing_shares":          existing_shares,
            "total_shares_after_drip":  round(total_shares_after, 8),
            "existing_cost_basis_usd":  existing_cost_basis,
            "total_cost_basis_usd":     round(total_cost_basis_after, 2),
            "new_cost_basis_per_share": new_cost_basis_per_share,
            "drip_execution_timestamp": now_utc.isoformat(),
        }

        return {
            "status":                   "success",
            "shares_purchased":         total_shares_purchased,
            "fractional_shares":        fractional_shares,
            "new_cost_basis_per_share": new_cost_basis_per_share,
            "reinvestment_summary":     reinvestment_summary,
            "timestamp":                now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"reit_dividend_reinvestment_logic failed: {e}")
        _log_lesson(f"reit_dividend_reinvestment_logic: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
