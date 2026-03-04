
"""
Executive Summary: Examines fee distributions to score congestion and recommend optimal bids.
Inputs: fees (list[dict]), block_utilization_pct (float)
Outputs: avg_fee (float), median_fee (float), fee_percentiles (dict), fee_trend (str), congestion_level (str), optimal_fee_estimate (float)
MCP Tool Name: transaction_fee_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "transaction_fee_analyzer",
    "description": "Analyzes fee samples and block utilization to guide transaction fee bidding.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fees": {
                "type": "array",
                "description": "List of fee datapoints {timestamp, fee_amount, gas_used, gas_price}.",
                "items": {
                    "type": "object",
                    "properties": {
                        "timestamp": {"type": "string", "description": "ISO timestamp"},
                        "fee_amount": {"type": "number", "description": "Fee paid in native token"},
                        "gas_used": {"type": "number", "description": "Gas units consumed"},
                        "gas_price": {"type": "number", "description": "Gas price in gwei or native units"}
                    },
                    "required": ["fee_amount", "gas_used", "gas_price"]
                }
            },
            "block_utilization_pct": {
                "type": "number",
                "description": "Current block utilization percentage (0-100)."
            }
        },
        "required": ["fees", "block_utilization_pct"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def transaction_fee_analyzer(**kwargs: Any) -> dict:
    """Computes descriptive statistics for the fee market and congestion labeling."""
    try:
        fees: Sequence[dict] = kwargs.get("fees", [])
        block_utilization = float(kwargs.get("block_utilization_pct", 0))
        if not fees:
            raise ValueError("fees list cannot be empty")
        fee_values = sorted(float(record["fee_amount"]) for record in fees)
        count = len(fee_values)
        avg_fee = sum(fee_values) / count
        median_fee = fee_values[count // 2]
        def percentile(pct: float) -> float:
            rank = max(0, min(count - 1, int(math.ceil((pct / 100) * count) - 1)))
            return fee_values[rank]
        fee_percentiles = {
            "p25": percentile(25),
            "p50": percentile(50),
            "p75": percentile(75),
            "p95": percentile(95)
        }
        fee_trend = "rising" if fee_values[-1] > fee_values[0] else "falling"
        if block_utilization >= 95:
            congestion_level = "severe"
        elif block_utilization >= 80:
            congestion_level = "high"
        elif block_utilization >= 60:
            congestion_level = "moderate"
        else:
            congestion_level = "light"
        optimal_fee_estimate = fee_percentiles["p75"] * (block_utilization / 100 + 1)
        return {
            "status": "success",
            "data": {
                "avg_fee": avg_fee,
                "median_fee": median_fee,
                "fee_percentiles": fee_percentiles,
                "fee_trend": fee_trend,
                "congestion_level": congestion_level,
                "optimal_fee_estimate": optimal_fee_estimate
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"transaction_fee_analyzer failed: {e}")
        _log_lesson(f"transaction_fee_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
