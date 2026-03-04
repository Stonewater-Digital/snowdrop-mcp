"""
Executive Summary: Current expected credit loss (CECL) calculation across portfolio segments with qualitative adjustments.
Inputs: loan_segments (list[dict])
Outputs: cecl_reserve (float), segment_reserves (list[dict]), coverage_ratio (float)
MCP Tool Name: cecl_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "cecl_calculator",
    "description": "Calculates CECL reserves by segment using life-of-loan loss rates plus qualitative adjustments.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "loan_segments": {
                "type": "array",
                "description": "Segments with balances and historical loss experience.",
                "items": {
                    "type": "object",
                    "properties": {
                        "segment": {"type": "string", "description": "Segment name"},
                        "outstanding_balance": {"type": "number", "description": "Current amortized cost"},
                        "historical_loss_rate_pct": {"type": "number", "description": "Life-of-loan historical loss rate"},
                        "economic_adjustment_pct": {"type": "number", "description": "Forward-looking adjustment"},
                        "qualitative_adjustment_pct": {"type": "number", "description": "Management Q-factor"},
                    },
                    "required": [
                        "segment",
                        "outstanding_balance",
                        "historical_loss_rate_pct",
                        "economic_adjustment_pct",
                        "qualitative_adjustment_pct",
                    ],
                },
            }
        },
        "required": ["loan_segments"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "CECL results"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def cecl_calculator(loan_segments: List[dict[str, Any]], **_: Any) -> dict[str, Any]:
    try:
        if not loan_segments:
            raise ValueError("loan_segments required")
        total_reserve = 0.0
        total_balance = 0.0
        reserves = []
        for entry in loan_segments:
            balance = entry["outstanding_balance"]
            total_balance += balance
            total_loss_rate = (
                entry["historical_loss_rate_pct"]
                + entry["economic_adjustment_pct"]
                + entry["qualitative_adjustment_pct"]
            ) / 100.0
            reserve = balance * total_loss_rate
            total_reserve += reserve
            reserves.append(
                {
                    "segment": entry["segment"],
                    "loss_rate_pct": round(total_loss_rate * 100, 2),
                    "reserve": round(reserve, 2),
                }
            )
        coverage = (total_reserve / total_balance) * 100 if total_balance else 0.0
        data = {
            "cecl_reserve": round(total_reserve, 2),
            "coverage_ratio_pct": round(coverage, 2),
            "segment_reserves": reserves,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"cecl_calculator failed: {e}")
        _log_lesson(f"cecl_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
