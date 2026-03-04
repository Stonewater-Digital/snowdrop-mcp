"""Classify commodity curve structure."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "contango_backwardation_detector",
    "description": (
        "Identifies curve structure (contango / backwardation / mixed), computes per-tenor "
        "annualized roll yield, front and tail basis, and flags extreme backwardation."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_price": {
                "type": "number",
                "description": "Current spot price (must be > 0).",
            },
            "futures_prices": {
                "type": "array",
                "description": "Futures contracts ordered by tenor.",
                "items": {
                    "type": "object",
                    "properties": {
                        "tenor_months": {
                            "type": "number",
                            "description": "Months to expiry (must be > 0).",
                        },
                        "price": {
                            "type": "number",
                            "description": "Futures contract price (must be > 0).",
                        },
                    },
                    "required": ["tenor_months", "price"],
                },
                "minItems": 1,
            },
        },
        "required": ["spot_price", "futures_prices"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "structure": {"type": "string", "enum": ["contango", "backwardation", "mixed"]},
            "front_basis": {"type": "number"},
            "tail_basis": {"type": "number"},
            "front_annualized_roll_yield_pct": {"type": "number"},
            "curve_points": {"type": "array"},
            "extreme_backwardation": {"type": "boolean"},
            "timestamp": {"type": "string"},
        },
    },
}


def contango_backwardation_detector(
    spot_price: float,
    futures_prices: Iterable[dict[str, float]],
    **_: Any,
) -> dict[str, Any]:
    """Return curve classification and roll metrics.

    Args:
        spot_price: Current spot price (must be > 0).
        futures_prices: Iterable of dicts with ``tenor_months`` and ``price`` keys.

    Returns:
        dict with status, structure, front/tail basis, front annualized roll yield,
        curve_points enriched with per-tenor roll yield, and extreme_backwardation flag.

    Roll yield formula (annualized):
        roll_yield = (S / F - 1) * (12 / T)
    where S = spot, F = futures price, T = months to expiry.

    Extreme backwardation flag fires when spot is > 5% above front contract.
    """
    try:
        ordered = sorted(futures_prices, key=lambda item: float(item["tenor_months"]))
        if not ordered:
            raise ValueError("futures_prices cannot be empty")
        if not isinstance(spot_price, (int, float)) or spot_price <= 0:
            raise ValueError("spot_price must be a positive number")
        for i, p in enumerate(ordered):
            if float(p["tenor_months"]) <= 0:
                raise ValueError(f"futures_prices[{i}].tenor_months must be > 0")
            if float(p["price"]) <= 0:
                raise ValueError(f"futures_prices[{i}].price must be > 0")

        first_price = float(ordered[0]["price"])
        last_price = float(ordered[-1]["price"])

        if first_price > spot_price and last_price >= first_price:
            structure = "contango"
        elif first_price < spot_price and last_price <= first_price:
            structure = "backwardation"
        else:
            structure = "mixed"

        # Annualized roll yield for front contract: (S/F - 1) * 12/T
        front_t = float(ordered[0]["tenor_months"])
        front_roll_yield = (spot_price / first_price - 1) * (12.0 / front_t)

        # Enrich curve points with per-tenor roll yield
        curve_points = []
        for p in ordered:
            t = float(p["tenor_months"])
            f = float(p["price"])
            roll = (spot_price / f - 1) * (12.0 / t)
            curve_points.append(
                {
                    "tenor_months": t,
                    "price": f,
                    "basis": round(f - spot_price, 4),
                    "annualized_roll_yield_pct": round(roll * 100, 3),
                }
            )

        # Extreme backwardation: spot > 5% above front futures
        extreme_backwardation = (spot_price / first_price - 1) > 0.05

        return {
            "status": "success",
            "structure": structure,
            "front_basis": round(first_price - spot_price, 4),
            "tail_basis": round(last_price - spot_price, 4),
            "front_annualized_roll_yield_pct": round(front_roll_yield * 100, 3),
            "curve_points": curve_points,
            "extreme_backwardation": extreme_backwardation,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("contango_backwardation_detector", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
