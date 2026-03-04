"""
Executive Summary: Tax-aware rebalancer computing optimal trades under capital gains budget and wash sale avoidance.
Inputs: positions (list[dict]), target_weights (dict[str, float]), long_term_rate (float), short_term_rate (float), tax_budget (float)
Outputs: trade_plan (list[dict]), realized_gains (dict), wash_sale_flags (list[str]), post_trade_allocations (list[dict])
MCP Tool Name: tax_aware_rebalancer
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "tax_aware_rebalancer",
    "description": (
        "Constructs a tax-lot aware rebalance plan that respects capital gains budgets, wash-sale windows, "
        "and differentiates long- vs short-term tax rates per IRS Publication 550 guidance."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "description": "List of positions with quantity, cost basis, and acquisition date.",
                "items": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Security identifier"},
                        "quantity": {"type": "number", "description": "Shares held"},
                        "current_price": {"type": "number", "description": "Market price"},
                        "cost_basis": {"type": "number", "description": "Per-share cost basis"},
                        "acquisition_date": {
                            "type": "string",
                            "description": "ISO date of original acquisition for holding-period test",
                        },
                    },
                    "required": ["ticker", "quantity", "current_price", "cost_basis", "acquisition_date"],
                },
            },
            "target_weights": {
                "type": "object",
                "description": "Desired post-trade weights keyed by ticker (must sum to <=1).",
                "additionalProperties": {"type": "number"},
            },
            "cash_allocation": {
                "type": "number",
                "description": "Optional target cash weight; residual allocated proportionally if omitted.",
            },
            "long_term_rate": {
                "type": "number",
                "description": "Tax rate applied to positions held > 365 days (decimal).",
            },
            "short_term_rate": {
                "type": "number",
                "description": "Tax rate applied to positions held <= 365 days (decimal).",
            },
            "tax_budget": {
                "type": "number",
                "description": "Maximum cash tax to realize for the rebalance; defaults unlimited.",
            },
            "as_of_date": {
                "type": "string",
                "description": "ISO-8601 date to evaluate holding period and wash sale window (default today).",
            },
        },
        "required": ["positions", "target_weights"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Trade guidance"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


ISO_FORMAT = "%Y-%m-%d"


def _parse(date_str: str) -> datetime:
    return datetime.strptime(date_str, ISO_FORMAT)


def _holding_period_days(acquired: str, as_of: datetime) -> int:
    return (as_of - _parse(acquired)).days


def tax_aware_rebalancer(
    positions: List[Dict[str, Any]],
    target_weights: Dict[str, float],
    cash_allocation: float | None = None,
    long_term_rate: float = 0.15,
    short_term_rate: float = 0.32,
    tax_budget: float | None = None,
    as_of_date: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not positions:
            raise ValueError("positions cannot be empty")
        as_of = datetime.fromisoformat(as_of_date) if as_of_date else datetime.today()
        total_value = sum(p["quantity"] * p["current_price"] for p in positions)
        if total_value <= 0:
            raise ValueError("Total portfolio value must be positive")
        if cash_allocation is None:
            cash_allocation = max(0.0, 1.0 - sum(target_weights.values()))
        wash_window = timedelta(days=30)
        trade_plan = []
        wash_flags = []
        realized_long = 0.0
        realized_short = 0.0
        for pos in positions:
            ticker = pos["ticker"]
            current_value = pos["quantity"] * pos["current_price"]
            target_value = total_value * target_weights.get(ticker, 0.0)
            delta_value = target_value - current_value
            if abs(delta_value) < 1e-4:
                continue
            shares = delta_value / pos["current_price"]
            gain_per_share = pos["current_price"] - pos["cost_basis"]
            holding_days = _holding_period_days(pos["acquisition_date"], as_of)
            long_term = holding_days > 365
            selling = shares < 0
            tax_cost = 0.0
            blocked = False
            if selling and gain_per_share < 0:
                if holding_days < wash_window.days:
                    blocked = True
                    wash_flags.append(ticker)
            if selling and not blocked:
                realized = -shares * pos["current_price"] * (gain_per_share / pos["current_price"])
                if gain_per_share >= 0:
                    realized = -shares * gain_per_share
                else:
                    realized = -shares * gain_per_share
                if gain_per_share >= 0:
                    tax_cost = realized * (long_term_rate if long_term else short_term_rate)
                    if long_term:
                        realized_long += realized
                    else:
                        realized_short += realized
                else:
                    tax_cost = realized * (long_term_rate if long_term else short_term_rate)
            if tax_budget is not None and tax_cost > 0 and (realized_long + realized_short) * long_term_rate > tax_budget:
                blocked = True
                wash_flags.append(f"Tax budget limit hit for {ticker}")
            trade_plan.append(
                {
                    "ticker": ticker,
                    "shares": round(float(0 if blocked else shares), 4),
                    "blocked": blocked,
                    "reason": "wash_sale" if blocked else None,
                    "tax_cost": round(tax_cost, 4),
                }
            )
        post_allocations = []
        value_after = 0.0
        for trade in trade_plan:
            ticker = trade["ticker"]
            pos = next(p for p in positions if p["ticker"] == ticker)
            shares = pos["quantity"] + trade["shares"]
            value = shares * pos["current_price"]
            value_after += value
            post_allocations.append({"ticker": ticker, "weight": round(value / total_value, 6)})
        realized_taxes = {
            "long_term_gain": round(realized_long, 2),
            "short_term_gain": round(realized_short, 2),
            "estimated_tax": round(realized_long * long_term_rate + realized_short * short_term_rate, 2),
        }
        data = {
            "trade_plan": trade_plan,
            "realized_gains": realized_taxes,
            "wash_sale_flags": wash_flags,
            "post_trade_allocations": post_allocations,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError) as e:
        logger.error(f"tax_aware_rebalancer failed: {e}")
        _log_lesson(f"tax_aware_rebalancer: {e}")
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
