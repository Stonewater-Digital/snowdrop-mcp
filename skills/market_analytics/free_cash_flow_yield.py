"""
Execuve Summary: Computes free cash flow yield versus earnings and dividend yields.
Inputs: operating_cash_flow (float), capex (float), stock_price (float), shares_outstanding (float), dividend_yield (float|None)
Outputs: fcf (float), fcf_per_share (float), fcf_yield (float), vs_earnings_yield (float|None), vs_dividend_yield (float|None)
MCP Tool Name: free_cash_flow_yield
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "free_cash_flow_yield",
    "description": "Derives free cash flow yield and compares against earnings/dividend yields when available.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operating_cash_flow": {"type": "number", "description": "Operating cash flow (annual)."},
            "capex": {"type": "number", "description": "Capital expenditures (annual)."},
            "stock_price": {"type": "number", "description": "Current share price."},
            "shares_outstanding": {"type": "number", "description": "Shares outstanding."},
            "dividend_yield": {"type": "number", "description": "Optional dividend yield."},
            "eps": {"type": "number", "description": "Optional EPS for earnings yield comparison."}
        },
        "required": ["operating_cash_flow", "capex", "stock_price", "shares_outstanding"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def free_cash_flow_yield(**kwargs: Any) -> dict:
    """Computes free cash flow yield and compares to other valuation yields."""
    try:
        ocf = kwargs.get("operating_cash_flow")
        capex = kwargs.get("capex")
        price = kwargs.get("stock_price")
        shares = kwargs.get("shares_outstanding")
        dividend_yield = kwargs.get("dividend_yield")
        eps = kwargs.get("eps")
        for label, value in (("operating_cash_flow", ocf), ("capex", capex), ("stock_price", price), ("shares_outstanding", shares)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if price <= 0 or shares <= 0:
            raise ValueError("stock_price and shares_outstanding must be positive")

        fcf = ocf - capex
        fcf_per_share = fcf / shares
        fcf_yield = fcf_per_share / price
        vs_earnings_yield = (eps / price - fcf_yield) if isinstance(eps, (int, float)) and price else None
        vs_dividend_yield = (fcf_yield - dividend_yield) if isinstance(dividend_yield, (int, float)) else None

        return {
            "status": "success",
            "data": {
                "fcf": fcf,
                "fcf_per_share": fcf_per_share,
                "fcf_yield": fcf_yield,
                "vs_earnings_yield": vs_earnings_yield,
                "vs_dividend_yield": vs_dividend_yield
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"free_cash_flow_yield failed: {e}")
        _log_lesson(f"free_cash_flow_yield: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
