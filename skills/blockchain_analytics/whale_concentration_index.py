
"""
Executive Summary: Quantifies wealth concentration among top addresses and decentralization health.
Inputs: balances (list[float])
Outputs: gini_coefficient (float), top_10_pct_held (float), top_100_pct_held (float), herfindahl_index (float), nakamoto_coefficient (int), decentralization_score (float)
MCP Tool Name: whale_concentration_index
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "whale_concentration_index",
    "description": "Evaluates distribution of balances to understand whale dominance and decentralization risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "balances": {
                "type": "array",
                "description": "List of wallet balances in descending order (raw tokens or USD).",
                "items": {"type": "number"}
            }
        },
        "required": ["balances"]
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


def whale_concentration_index(**kwargs: Any) -> dict:
    """Computes Gini, Herfindahl, and Nakamoto concentration metrics."""
    try:
        balances: Sequence[float] = kwargs.get("balances", [])
        if not isinstance(balances, Sequence) or not balances:
            raise ValueError("balances must be a non-empty list of numbers")
        ordered = [float(b) for b in balances if float(b) >= 0]
        if not ordered:
            raise ValueError("balances must contain non-negative numbers")
        total = sum(ordered)
        if total == 0:
            raise ZeroDivisionError("Total balance cannot be zero")
        normalized = [bal / total for bal in ordered]
        cumulative = 0
        gini_sum = 0
        for i, value in enumerate(normalized, start=1):
            cumulative += value
            gini_sum += cumulative
        gini_coefficient = 1 - 2 * gini_sum / len(normalized)
        top_10_pct = sum(ordered[:max(1, len(ordered) // 10)]) / total * 100
        top_100_pct = sum(ordered[:min(100, len(ordered))]) / total * 100
        herfindahl_index = sum(p ** 2 for p in normalized)
        cumulative_share = 0
        nakamoto_coefficient = 0
        for share in normalized:
            cumulative_share += share
            nakamoto_coefficient += 1
            if cumulative_share >= 0.5:
                break
        decentralization_score = max(0.0, 100 - (top_10_pct * 0.5 + herfindahl_index * 100))
        return {
            "status": "success",
            "data": {
                "gini_coefficient": gini_coefficient,
                "top_10_pct_held": top_10_pct,
                "top_100_pct_held": top_100_pct,
                "herfindahl_index": herfindahl_index,
                "nakamoto_coefficient": nakamoto_coefficient,
                "decentralization_score": decentralization_score
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"whale_concentration_index failed: {e}")
        _log_lesson(f"whale_concentration_index: {e}")
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
