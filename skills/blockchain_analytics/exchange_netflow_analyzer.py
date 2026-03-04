
"""
Executive Summary: Tracks exchange inflow/outflow trends to infer accumulation vs distribution pressure.
Inputs: inflows (list[dict]), outflows (list[dict])
Outputs: net_flow_7d (float), accumulation_distribution_signal (str), exchange_balance_trend (str), sell_pressure_indicator (float), outflow_ratio (float)
MCP Tool Name: exchange_netflow_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "exchange_netflow_analyzer",
    "description": "Summarizes exchange wallet activity for accumulation/distribution signal generation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "inflows": {
                "type": "array",
                "description": "List of inflow records {timestamp, amount}. Amounts can be raw tokens.",
                "items": {
                    "type": "object",
                    "properties": {
                        "timestamp": {"type": "string", "description": "ISO timestamp."},
                        "amount": {"type": "number", "description": "Amount moving into exchanges."}
                    },
                    "required": ["timestamp", "amount"]
                }
            },
            "outflows": {
                "type": "array",
                "description": "List of outflow records {timestamp, amount}.",
                "items": {
                    "type": "object",
                    "properties": {
                        "timestamp": {"type": "string", "description": "ISO timestamp."},
                        "amount": {"type": "number", "description": "Amount moving out of exchanges."}
                    },
                    "required": ["timestamp", "amount"]
                }
            }
        },
        "required": ["inflows", "outflows"]
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


def exchange_netflow_analyzer(**kwargs: Any) -> dict:
    """Aggregates inflow/outflow data to infer net flows and sell pressure."""
    try:
        inflows: Sequence[dict] = kwargs.get("inflows", [])
        outflows: Sequence[dict] = kwargs.get("outflows", [])
        if not inflows and not outflows:
            raise ValueError("At least one inflow or outflow entry is required")
        total_in = sum(float(record.get("amount", 0)) for record in inflows)
        total_out = sum(float(record.get("amount", 0)) for record in outflows)
        net_flow_7d = total_in - total_out
        if abs(net_flow_7d) < 1e-6:
            accumulation_distribution_signal = "neutral"
        elif net_flow_7d < 0:
            accumulation_distribution_signal = "accumulation"
        else:
            accumulation_distribution_signal = "distribution"
        exchange_balance_trend = "declining" if accumulation_distribution_signal == "accumulation" else "rising"
        total_flow = total_in + total_out
        sell_pressure_indicator = (total_in / total_flow * 100) if total_flow else 0.0
        outflow_ratio = (total_out / total_flow * 100) if total_flow else 0.0
        return {
            "status": "success",
            "data": {
                "net_flow_7d": net_flow_7d,
                "accumulation_distribution_signal": accumulation_distribution_signal,
                "exchange_balance_trend": exchange_balance_trend,
                "sell_pressure_indicator": sell_pressure_indicator,
                "outflow_ratio": outflow_ratio
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"exchange_netflow_analyzer failed: {e}")
        _log_lesson(f"exchange_netflow_analyzer: {e}")
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
