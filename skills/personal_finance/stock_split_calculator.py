"""
Executive Smary: Adjusts share count and cost basis for stock splits.
Inputs: pre_split_shares (float), pre_split_price (float), split_ratio (str)
Outputs: post_split_shares (float), post_split_price (float), adjusted_cost_basis (float), total_value (float)
MCP Tool Name: stock_split_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")


def _parse_ratio(ratio: str) -> tuple[float, float]:
    parts = ratio.split(":")
    if len(parts) != 2:
        raise ValueError("split_ratio must be formatted like '4:1'")
    new = float(parts[0])
    old = float(parts[1])
    if new <= 0 or old <= 0:
        raise ValueError("split_ratio terms must be positive")
    return new, old


TOOL_META = {
    "name": "stock_split_calculator",
    "description": (
        "Computes the new share count and per-share price after a split while keeping "
        "total value and cost basis aligned."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "pre_split_shares": {
                "type": "number",
                "description": "Share count before the split.",
            },
            "pre_split_price": {
                "type": "number",
                "description": "Share price before the split.",
            },
            "split_ratio": {
                "type": "string",
                "description": "Split ratio formatted like '4:1' or '1:5'.",
            },
        },
        "required": ["pre_split_shares", "pre_split_price", "split_ratio"],
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


def stock_split_calculator(**kwargs: Any) -> dict:
    """Adjust sharing pricing after a forward or reverse stock split."""
    try:
        shares = float(kwargs["pre_split_shares"])
        price = float(kwargs["pre_split_price"])
        ratio_str = str(kwargs["split_ratio"])

        if shares <= 0 or price <= 0:
            raise ValueError("Shares and price must be positive")

        new_ratio, old_ratio = _parse_ratio(ratio_str)
        post_shares = shares * (new_ratio / old_ratio)
        post_price = price * (old_ratio / new_ratio)
        total_value = post_shares * post_price
        adjusted_cost_basis = price * shares / post_shares if post_shares > 0 else 0.0

        return {
            "status": "success",
            "data": {
                "post_split_shares": post_shares,
                "post_split_price": post_price,
                "adjusted_cost_basis": adjusted_cost_basis,
                "total_value": total_value,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"stock_split_calculator failed: {e}")
        _log_lesson(f"stock_split_calculator: {e}")
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
