"""
Execuve Summary: Evaluates book and tangible book values relative to market price.
Inputs: total_assets (float), total_liabilities (float), intangibles (float), goodwill (float), shares_outstanding (float), stock_price (float)
Outputs: book_value_per_share (float), tangible_book_per_share (float), pb_ratio (float), ptb_ratio (float), roe_implied (float)
MCP Tool Name: book_value_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "book_value_analyzer",
    "description": "Computes book/tangible book per share and related valuation ratios.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_assets": {"type": "number", "description": "Total assets."},
            "total_liabilities": {"type": "number", "description": "Total liabilities."},
            "intangibles": {"type": "number", "description": "Intangible assets."},
            "goodwill": {"type": "number", "description": "Goodwill on balance sheet."},
            "shares_outstanding": {"type": "number", "description": "Shares outstanding."},
            "stock_price": {"type": "number", "description": "Current share price."}
        },
        "required": ["total_assets", "total_liabilities", "intangibles", "goodwill", "shares_outstanding", "stock_price"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def book_value_analyzer(**kwargs: Any) -> dict:
    """Calculates book metrics per share and simple implied ROE signal."""
    try:
        assets = kwargs.get("total_assets")
        liabilities = kwargs.get("total_liabilities")
        intangibles = kwargs.get("intangibles")
        goodwill = kwargs.get("goodwill")
        shares = kwargs.get("shares_outstanding")
        price = kwargs.get("stock_price")
        for label, value in (("total_assets", assets), ("total_liabilities", liabilities), ("intangibles", intangibles), ("goodwill", goodwill), ("shares_outstanding", shares), ("stock_price", price)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if shares <= 0:
            raise ValueError("shares_outstanding must be positive")

        equity = assets - liabilities
        book_per_share = equity / shares
        tangible_equity = equity - intangibles - goodwill
        tangible_book_per_share = tangible_equity / shares
        pb_ratio = price / book_per_share if book_per_share else math.inf
        ptb_ratio = price / tangible_book_per_share if tangible_book_per_share else math.inf
        roe_implied = price / book_per_share - 1 if book_per_share else math.inf

        return {
            "status": "success",
            "data": {
                "book_value_per_share": book_per_share,
                "tangible_book_per_share": tangible_book_per_share,
                "pb_ratio": pb_ratio,
                "ptb_ratio": ptb_ratio,
                "roe_implied": roe_implied
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"book_value_analyzer failed: {e}")
        _log_lesson(f"book_value_analyzer: {e}")
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
