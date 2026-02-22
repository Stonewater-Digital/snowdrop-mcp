"""
Executive Summary: Server-location-based trade routing — selects the lowest-latency, high-reliability exchange route.
Inputs: order (dict: exchange str, token_pair str, amount float, side str),
        server_locations (list of dicts: exchange str, region str, latency_ms float, reliability_pct float)
Outputs: optimal_route (dict), latency_ms (float), alternatives (list), estimated_advantage_ms (float)
MCP Tool Name: latency_optimized_order_routing
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "latency_optimized_order_routing",
    "description": (
        "Selects the optimal server route for a trade order by ranking available "
        "exchange server locations by latency and filtering out unreliable routes "
        "(reliability < 99%). Returns the winning route, ranked alternatives, and "
        "estimated execution time advantage over the median route."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "order": {
                "type": "object",
                "properties": {
                    "exchange":    {"type": "string"},
                    "token_pair":  {"type": "string"},
                    "amount":      {"type": "number"},
                    "side":        {"type": "string", "enum": ["buy", "sell"]},
                },
                "required": ["exchange", "token_pair", "amount", "side"],
            },
            "server_locations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "exchange":       {"type": "string"},
                        "region":         {"type": "string"},
                        "latency_ms":     {"type": "number"},
                        "reliability_pct": {"type": "number"},
                    },
                    "required": ["exchange", "region", "latency_ms", "reliability_pct"],
                },
            },
        },
        "required": ["order", "server_locations"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "optimal_route":         {"type": "object"},
            "latency_ms":            {"type": "number"},
            "alternatives":          {"type": "array"},
            "estimated_advantage_ms": {"type": "number"},
            "status":                {"type": "string"},
            "timestamp":             {"type": "string"},
        },
        "required": ["optimal_route", "latency_ms", "alternatives", "estimated_advantage_ms", "status", "timestamp"],
    },
}

RELIABILITY_THRESHOLD_PCT: float = 99.0


def latency_optimized_order_routing(
    order: dict[str, Any],
    server_locations: list[dict[str, Any]],
) -> dict[str, Any]:
    """Route a trade order through the lowest-latency, reliable exchange server.

    Args:
        order: Trade order details with keys:
            - exchange (str): Target exchange name.
            - token_pair (str): Asset pair, e.g. "BTC/USDT".
            - amount (float): Order size.
            - side (str): "buy" or "sell".
        server_locations: List of available server nodes. Each dict contains:
            - exchange (str): Exchange this node serves.
            - region (str): Geographic region identifier.
            - latency_ms (float): Round-trip latency in milliseconds.
            - reliability_pct (float): Uptime reliability percentage (0–100).

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - optimal_route (dict): The winning server location entry.
            - latency_ms (float): Latency of the selected route.
            - alternatives (list[dict]): Remaining qualifying routes, ranked.
            - estimated_advantage_ms (float): Savings vs. median qualifying route latency.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        target_exchange: str = order.get("exchange", "").lower()

        # Filter to servers that match the target exchange and meet reliability threshold
        qualifying: list[dict[str, Any]] = [
            loc for loc in server_locations
            if loc.get("exchange", "").lower() == target_exchange
            and loc.get("reliability_pct", 0.0) >= RELIABILITY_THRESHOLD_PCT
        ]

        if not qualifying:
            # Fall back to any server meeting reliability threshold across all exchanges
            qualifying = [
                loc for loc in server_locations
                if loc.get("reliability_pct", 0.0) >= RELIABILITY_THRESHOLD_PCT
            ]

        if not qualifying:
            return {
                "status":                "error",
                "error":                 "No server locations meet the 99% reliability threshold.",
                "optimal_route":         {},
                "latency_ms":            0.0,
                "alternatives":          [],
                "estimated_advantage_ms": 0.0,
                "timestamp":             datetime.now(timezone.utc).isoformat(),
            }

        # Sort ascending by latency — best route first
        qualifying.sort(key=lambda loc: loc.get("latency_ms", float("inf")))

        optimal_route: dict[str, Any] = qualifying[0]
        optimal_latency: float = float(optimal_route.get("latency_ms", 0.0))
        alternatives: list[dict[str, Any]] = qualifying[1:]

        # Estimated advantage: difference between selected route and median route latency
        all_latencies: list[float] = [loc.get("latency_ms", 0.0) for loc in qualifying]
        n: int = len(all_latencies)
        sorted_latencies: list[float] = sorted(all_latencies)
        if n % 2 == 1:
            median_latency: float = sorted_latencies[n // 2]
        else:
            median_latency = (sorted_latencies[n // 2 - 1] + sorted_latencies[n // 2]) / 2.0

        estimated_advantage_ms: float = round(median_latency - optimal_latency, 4)

        return {
            "status":                "success",
            "optimal_route":         optimal_route,
            "latency_ms":            optimal_latency,
            "alternatives":          alternatives,
            "estimated_advantage_ms": estimated_advantage_ms,
            "timestamp":             datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"latency_optimized_order_routing failed: {e}")
        _log_lesson(f"latency_optimized_order_routing: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
