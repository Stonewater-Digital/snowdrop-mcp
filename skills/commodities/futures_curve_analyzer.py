"""Analyze futures term structure for commodities."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "futures_curve_analyzer",
    "description": (
        "Classifies contango/backwardation, computes annualized roll yield per tenor, "
        "implied cost of carry, and carry trade signal from spot + futures curve."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_price": {
                "type": "number",
                "description": "Current spot price of the commodity (must be > 0).",
            },
            "futures": {
                "type": "array",
                "description": "List of futures contracts sorted or unsorted by expiry.",
                "items": {
                    "type": "object",
                    "properties": {
                        "expiry_month": {
                            "type": "number",
                            "description": "Months to expiry from today (must be > 0).",
                        },
                        "price": {
                            "type": "number",
                            "description": "Futures price for this contract.",
                        },
                    },
                    "required": ["expiry_month", "price"],
                },
                "minItems": 1,
            },
            "storage_cost_pct_annual": {
                "type": ["number", "null"],
                "default": None,
                "description": "Annual storage cost as % of spot (optional, for cost-of-carry).",
            },
            "convenience_yield_pct_annual": {
                "type": ["number", "null"],
                "default": None,
                "description": "Annual convenience yield as % (optional, for cost-of-carry).",
            },
            "risk_free_rate_pct_annual": {
                "type": ["number", "null"],
                "default": None,
                "description": "Annual risk-free rate as % (optional, for theoretical forward).",
            },
        },
        "required": ["spot_price", "futures"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "structure": {
                "type": "string",
                "enum": ["contango", "backwardation", "mixed"],
            },
            "basis_by_tenor": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tenor_months": {"type": "number"},
                        "price": {"type": "number"},
                        "basis": {"type": "number"},
                        "annualized_roll_yield_pct": {"type": "number"},
                    },
                },
            },
            "front_annualized_roll_yield_pct": {"type": "number"},
            "cost_of_carry_pct_annual": {"type": ["number", "null"]},
            "theoretical_forward": {"type": ["number", "null"]},
            "carry_trade_signal": {"type": "string"},
            "timestamp": {"type": "string"},
        },
    },
}


def futures_curve_analyzer(
    spot_price: float,
    futures: list[dict[str, Any]],
    storage_cost_pct_annual: float | None = None,
    convenience_yield_pct_annual: float | None = None,
    risk_free_rate_pct_annual: float | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Classify curve structure, compute per-tenor roll yield, and report carry signal.

    Args:
        spot_price: Current spot price (must be > 0).
        futures: List of dicts with keys ``expiry_month`` (months > 0) and ``price``.
        storage_cost_pct_annual: Annual storage cost as % of spot (e.g. 2.0 = 2%).
        convenience_yield_pct_annual: Annual convenience yield as % (e.g. 3.0 = 3%).
        risk_free_rate_pct_annual: Annual risk-free rate as % for theoretical forward price.

    Returns:
        dict with status, structure classification, per-tenor basis/roll yield,
        cost-of-carry estimate, and carry trade signal.

    Roll yield per contract is annualized as:
        roll_yield = (S/F - 1) * (12 / T)
    where T = months to expiry, reflecting the annualized gain from rolling a
    short-dated future at spot and capturing the basis.

    Cost of carry uses the commodity pricing identity:
        F = S * exp((r + u - y) * T)  =>  cost_of_carry = r + u - y
    where r = risk-free rate, u = storage cost rate, y = convenience yield.
    """
    try:
        if not isinstance(spot_price, (int, float)) or spot_price <= 0:
            raise ValueError("spot_price must be a positive number")
        if not futures:
            raise ValueError("futures list cannot be empty")

        ordered = sorted(futures, key=lambda f: float(f["expiry_month"]))

        for i, fut in enumerate(ordered):
            if float(fut["expiry_month"]) <= 0:
                raise ValueError(f"futures[{i}].expiry_month must be > 0")
            if float(fut["price"]) <= 0:
                raise ValueError(f"futures[{i}].price must be > 0")

        # Per-tenor roll yield: annualized return from holding spot vs rolling futures
        basis_by_tenor = []
        for fut in ordered:
            t_months = float(fut["expiry_month"])
            f_price = float(fut["price"])
            basis = f_price - spot_price
            # Annualized roll yield = (S/F - 1) * (12/T)
            # Positive in backwardation (F < S), negative in contango (F > S)
            roll_yield_annual = (spot_price / f_price - 1) * (12.0 / t_months)
            basis_by_tenor.append(
                {
                    "tenor_months": t_months,
                    "price": f_price,
                    "basis": round(basis, 4),
                    "annualized_roll_yield_pct": round(roll_yield_annual * 100, 3),
                }
            )

        front = ordered[0]
        back = ordered[-1]
        front_price = float(front["price"])
        back_price = float(back["price"])

        # Structure classification: requires monotonic contango or backwardation
        if front_price > spot_price and back_price >= front_price:
            structure = "contango"
        elif front_price < spot_price and back_price <= front_price:
            structure = "backwardation"
        else:
            structure = "mixed"

        front_roll = basis_by_tenor[0]["annualized_roll_yield_pct"]

        # Cost of carry: c = r + u - y (all as annual decimals)
        cost_of_carry: float | None = None
        if any(v is not None for v in [storage_cost_pct_annual, convenience_yield_pct_annual, risk_free_rate_pct_annual]):
            r = (risk_free_rate_pct_annual or 0.0) / 100
            u = (storage_cost_pct_annual or 0.0) / 100
            y = (convenience_yield_pct_annual or 0.0) / 100
            cost_of_carry = round((r + u - y) * 100, 3)

        # Theoretical forward for front contract using F = S * exp(c * T/12)
        theoretical_forward: float | None = None
        if cost_of_carry is not None:
            t_years = float(front["expiry_month"]) / 12.0
            theoretical_forward = round(spot_price * math.exp((cost_of_carry / 100) * t_years), 4)

        carry_signal = (
            "short_front_long_deferred"
            if structure == "contango"
            else "long_front_short_deferred"
            if structure == "backwardation"
            else "no_clear_signal"
        )

        return {
            "status": "success",
            "structure": structure,
            "basis_by_tenor": basis_by_tenor,
            "front_annualized_roll_yield_pct": front_roll,
            "cost_of_carry_pct_annual": cost_of_carry,
            "theoretical_forward": theoretical_forward,
            "carry_trade_signal": carry_signal,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("futures_curve_analyzer", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
