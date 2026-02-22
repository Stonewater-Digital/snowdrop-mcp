"""Evaluate multi-leg option strategies over a price range."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "options_strategy_analyzer",
    "description": "Aggregates multi-leg option strategy P&L and diagnostics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "legs": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Option legs with type, direction, strike, premium, quantity.",
            },
            "spot_price": {"type": "number"},
            "price_range_pct": {
                "type": "number",
                "default": 0.30,
                "description": "Symmetric percent band to sweep underlying prices.",
            },
        },
        "required": ["legs", "spot_price"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


DefLeg = dict[str, Any]


def options_strategy_analyzer(
    legs: list[DefLeg],
    spot_price: float,
    price_range_pct: float = 0.30,
    **_: Any,
) -> dict[str, Any]:
    """Analyze expiry P&L for an option strategy."""
    try:
        if spot_price <= 0:
            raise ValueError("spot_price must be positive")
        if not legs:
            raise ValueError("At least one leg required")
        if price_range_pct <= 0:
            raise ValueError("price_range_pct must be positive")

        min_price = max(0.01, spot_price * (1 - price_range_pct))
        max_price = spot_price * (1 + price_range_pct)
        steps = 41
        price_points = [min_price + i * (max_price - min_price) / (steps - 1) for i in range(steps)]

        pnl_curve = []
        for price in price_points:
            pnl = sum(_leg_payoff(leg, price) for leg in legs)
            pnl_curve.append({"underlying_price": round(price, 4), "pnl": round(pnl, 4)})

        pnls = [point["pnl"] for point in pnl_curve]
        max_profit_value = max(pnls)
        min_profit_value = min(pnls)
        unlimited_profit = pnls[-1] > pnls[-2] or pnls[0] > pnls[1]
        max_profit: float | str = round(max_profit_value, 4)
        if unlimited_profit and max_profit_value in {pnls[-1], pnls[0]}:
            max_profit = "unlimited"

        break_evens = _estimate_break_even_prices(price_points, pnls)
        strategy_name = _detect_strategy(legs)

        data = {
            "max_profit": max_profit,
            "max_loss": round(min_profit_value, 4),
            "break_even_prices": break_evens,
            "pnl_at_expiry": pnl_curve,
            "strategy_name": strategy_name,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("options_strategy_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _leg_payoff(leg: DefLeg, price: float) -> float:
    option_type = leg.get("type", "").lower()
    direction = leg.get("direction", "long").lower()
    quantity = float(leg.get("quantity", 1))
    premium = float(leg.get("premium", 0))
    strike = float(leg.get("strike"))

    intrinsic = 0.0
    if option_type == "call":
        intrinsic = max(0.0, price - strike)
    elif option_type == "put":
        intrinsic = max(0.0, strike - price)
    else:
        raise ValueError(f"Unsupported option type: {option_type}")

    direction_mult = 1.0 if direction == "long" else -1.0
    pnl = direction_mult * quantity * (intrinsic - premium)
    return pnl


def _estimate_break_even_prices(prices: Iterable[float], pnls: list[float]) -> list[float]:
    prices_list = list(prices)
    break_evens: set[float] = set()
    for idx in range(1, len(pnls)):
        p_prev, p_curr = pnls[idx - 1], pnls[idx]
        if p_prev == 0:
            break_evens.add(round(prices_list[idx - 1], 4))
            continue
        if p_prev * p_curr < 0:
            price_prev = prices_list[idx - 1]
            price_curr = prices_list[idx]
            slope = (p_curr - p_prev) / (price_curr - price_prev)
            if slope == 0:
                continue
            root = price_prev - p_prev / slope
            break_evens.add(round(root, 4))
    return sorted(break_evens)


def _detect_strategy(legs: list[DefLeg]) -> str:
    types = [leg.get("type", "").lower() for leg in legs]
    directions = [leg.get("direction", "long").lower() for leg in legs]
    strikes = [leg.get("strike") for leg in legs]

    if (
        len(legs) == 2
        and set(types) == {"call", "put"}
        and all(dir_ == "long" for dir_ in directions)
        and strikes[0] == strikes[1]
    ):
        return "straddle"
    if (
        len(legs) == 2
        and set(types) == {"call", "put"}
        and all(dir_ == "long" for dir_ in directions)
        and strikes[0] != strikes[1]
    ):
        return "strangle"

    call_count = types.count("call")
    put_count = types.count("put")
    long_count = directions.count("long")
    short_count = directions.count("short")
    if len(legs) == 4 and call_count == 2 and put_count == 2 and long_count == 2 and short_count == 2:
        return "iron_condor"

    if len(legs) == 2 and len(set(types)) == 1 and {"long", "short"}.issubset(set(directions)):
        return "vertical_spread"

    return "custom_strategy"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
