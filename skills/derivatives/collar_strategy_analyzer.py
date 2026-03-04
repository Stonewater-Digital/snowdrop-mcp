"""Zero-cost collar analyzer."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "collar_strategy_analyzer",
    "description": "Analyzes protective collar payoff, net cost, and protection ranges.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_price": {"type": "number", "description": "Current stock price. Must be > 0."},
            "put_strike": {"type": "number", "description": "Put strike (floor). Must be > 0."},
            "call_strike": {"type": "number", "description": "Call strike (cap). Must be > put_strike."},
            "put_premium": {"type": "number", "description": "Put premium paid per share. Must be >= 0."},
            "call_premium": {"type": "number", "description": "Call premium received per share. Must be >= 0."},
            "shares": {"type": "number", "default": 100.0, "description": "Number of shares (default 100)."},
        },
        "required": ["spot_price", "put_strike", "call_strike", "put_premium", "call_premium"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "net_premium": {"type": "number"},
                    "net_cost": {"type": "number"},
                    "downside_protection_pct": {"type": "number"},
                    "upside_cap_pct": {"type": "number"},
                    "effective_cost_of_protection_pct": {"type": "number"},
                    "break_even_at_expiry": {"type": "number"},
                    "is_zero_cost": {"type": "boolean"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def collar_strategy_analyzer(
    spot_price: float,
    put_strike: float,
    call_strike: float,
    put_premium: float,
    call_premium: float,
    shares: float = 100.0,
    **_: Any,
) -> dict[str, Any]:
    """Return collar economics: net cost, protection range, and breakeven.

    A collar = long stock + long put + short call.
    Net premium = put_premium - call_premium  (positive = net cost, negative = net credit).
    Break-even = spot_price + net_premium (adjusted cost basis per share).

    Args:
        spot_price: Current stock price (must be > 0).
        put_strike: Downside protection floor (must be > 0).
        call_strike: Upside cap (should be > put_strike).
        put_premium: Premium paid per share for the put (must be >= 0).
        call_premium: Premium received per share for the call (must be >= 0).
        shares: Number of shares covered (default 100).

    Returns:
        dict with net_premium, net_cost, downside_protection_pct,
        upside_cap_pct, effective_cost_of_protection_pct,
        break_even_at_expiry, is_zero_cost.
    """
    try:
        if spot_price <= 0:
            raise ValueError("spot_price must be positive")
        if put_strike <= 0 or call_strike <= 0:
            raise ValueError("put_strike and call_strike must be positive")
        if put_premium < 0 or call_premium < 0:
            raise ValueError("premiums must be non-negative")
        if call_strike <= put_strike:
            raise ValueError("call_strike should be greater than put_strike")
        if shares <= 0:
            raise ValueError("shares must be positive")

        # Net premium per share (positive = net debit)
        net_premium_per_share = put_premium - call_premium
        net_premium = net_premium_per_share * shares

        # Downside: from spot to put floor
        downside_protection_pct = (1 - put_strike / spot_price) * 100

        # Upside: from spot to call cap
        upside_cap_pct = (call_strike / spot_price - 1) * 100

        # Break-even at expiry: cost basis = spot + net_premium_per_share
        break_even = spot_price + net_premium_per_share

        # Effective cost of protection as % of position value
        position_value = spot_price * shares
        effective_cost_pct = (net_premium / position_value) * 100

        is_zero_cost = abs(net_premium_per_share) < 1e-6

        data = {
            "net_premium": round(net_premium, 2),
            "net_cost": round(net_premium, 2),
            "downside_protection_pct": round(downside_protection_pct, 2),
            "upside_cap_pct": round(upside_cap_pct, 2),
            "effective_cost_of_protection_pct": round(effective_cost_pct, 4),
            "break_even_at_expiry": round(break_even, 4),
            "is_zero_cost": is_zero_cost,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson(f"collar_strategy_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
