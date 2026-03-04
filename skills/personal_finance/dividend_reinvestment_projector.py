"""
Executive Smary: Models DRIP growth over time with dividend and price appreciation.
Inputs: initial_shares (float), share_price (float), annual_dividend_per_share (float), dividend_growth_rate (float), years (int), price_growth_rate (float)
Outputs: ending_shares (float), ending_value (float), total_dividends_received (float), yield_on_cost (float), year_by_year (list)
MCP Tool Name: dividend_reinvestment_projector
"""
import logging
from datetime import datetime, timezone
from typing import Any, List, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "dividend_reinvestment_projector",
    "description": (
        "Projects a dividend reinvestment plan by compounding dividends into new shares "
        "with growth assumptions for payouts and share price."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "initial_shares": {
                "type": "number",
                "description": "Starting share count.",
            },
            "share_price": {
                "type": "number",
                "description": "Current share price in dollars.",
            },
            "annual_dividend_per_share": {
                "type": "number",
                "description": "Current annual dividend per share.",
            },
            "dividend_growth_rate": {
                "type": "number",
                "description": "Expected annual dividend growth rate as decimal.",
            },
            "years": {
                "type": "number",
                "description": "Projection horizon in years.",
            },
            "price_growth_rate": {
                "type": "number",
                "description": "Annual share price growth rate as decimal.",
            },
        },
        "required": [
            "initial_shares",
            "share_price",
            "annual_dividend_per_share",
            "dividend_growth_rate",
            "years",
            "price_growth_rate",
        ],
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


def dividend_reinvestment_projector(**kwargs: Any) -> dict:
    """Project DRIP performance over the requested term."""
    try:
        shares = float(kwargs["initial_shares"])
        share_price = float(kwargs["share_price"])
        dividend = float(kwargs["annual_dividend_per_share"])
        dividend_growth = float(kwargs["dividend_growth_rate"])
        years = int(kwargs["years"])
        price_growth = float(kwargs["price_growth_rate"])

        if shares < 0 or share_price <= 0 or years <= 0:
            raise ValueError("Provide positive share price and years along with non-negative shares")

        total_dividends = 0.0
        year_by_year: List[Dict[str, Any]] = []
        cost_basis = shares * share_price

        for year in range(1, years + 1):
            price = share_price * (1 + price_growth) ** (year - 1)
            dividend_per_share = dividend * (1 + dividend_growth) ** (year - 1)
            dividends = shares * dividend_per_share
            total_dividends += dividends
            new_shares = dividends / price
            shares += new_shares
            value = shares * price
            year_by_year.append(
                {
                    "year": year,
                    "share_price": price,
                    "dividend_per_share": dividend_per_share,
                    "dividends_reinvested": dividends,
                    "shares": shares,
                    "portfolio_value": value,
                }
            )

        ending_price = share_price * (1 + price_growth) ** (years - 1)
        ending_value = shares * ending_price
        yield_on_cost = (
            (total_dividends / cost_basis) if cost_basis > 0 else 0.0
        )

        return {
            "status": "success",
            "data": {
                "ending_shares": shares,
                "ending_value": ending_value,
                "total_dividends_received": total_dividends,
                "yield_on_cost": yield_on_cost,
                "year_by_year": year_by_year,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"dividend_reinvestment_projector failed: {e}")
        _log_lesson(f"dividend_reinvestment_projector: {e}")
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
