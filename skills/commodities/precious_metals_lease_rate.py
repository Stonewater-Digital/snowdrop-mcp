"""Infer precious metal lease rates."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "precious_metals_lease_rate",
    "description": (
        "Derives the implied precious metals lease rate from spot, forward, and USD interest rate "
        "inputs. Uses the GOFO (Gold Forward Offered Rate) identity: "
        "Lease Rate = USD Rate − GOFO, where GOFO = annualized forward premium."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_price": {
                "type": "number",
                "description": "Spot price of the metal in USD/oz (must be > 0).",
            },
            "forward_price": {
                "type": "number",
                "description": "Forward price of the metal in USD/oz for the given tenor (must be > 0).",
            },
            "tenor_days": {
                "type": "number",
                "description": "Tenor of the forward contract in calendar days (must be > 0).",
            },
            "usd_rate_pct": {
                "type": "number",
                "description": "Annualized USD LIBOR/SOFR interest rate as % for the same tenor.",
            },
        },
        "required": ["spot_price", "forward_price", "tenor_days", "usd_rate_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "gofo_pct": {"type": "number"},
            "lease_rate_pct": {"type": "number"},
            "forward_premium_pct": {"type": "number"},
            "contango_flag": {"type": "boolean"},
            "timestamp": {"type": "string"},
        },
    },
}


def precious_metals_lease_rate(
    spot_price: float,
    forward_price: float,
    tenor_days: float,
    usd_rate_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return GOFO and implied lease rate from precious metals forward pricing.

    Args:
        spot_price: Metal spot price in USD/oz (must be > 0).
        forward_price: Metal forward price in USD/oz (must be > 0).
        tenor_days: Forward contract tenor in calendar days (must be > 0).
        usd_rate_pct: Annualized USD interest rate for the same tenor as %.

    Returns:
        dict with status, gofo_pct, lease_rate_pct, forward_premium_pct, contango_flag.

    Formulas:
        Forward premium (continuous, annualized):
            GOFO = ln(F / S) * (365 / T)

        Lease rate (the borrowing cost for the metal):
            Lease Rate = USD Rate - GOFO

        Identity (cost-of-carry for precious metals):
            F = S * exp((USD_rate - lease_rate) * T/365)

        Positive GOFO = forward > spot = contango (normal for gold/silver when rates > lease rates).
        Negative GOFO = backwardation = lease rates > USD rates (unusual, signals metal shortage).
    """
    try:
        if spot_price <= 0:
            raise ValueError("spot_price must be positive")
        if forward_price <= 0:
            raise ValueError("forward_price must be positive")
        if tenor_days <= 0:
            raise ValueError("tenor_days must be positive")

        t_years = tenor_days / 365.0

        # GOFO (Gold Forward Offered Rate) = continuously compounded annualized forward premium
        gofo = math.log(forward_price / spot_price) / t_years
        gofo_pct = gofo * 100.0

        # Lease rate = USD rate - GOFO
        lease_rate_pct = usd_rate_pct - gofo_pct

        # Simple forward premium for context
        forward_premium_pct = (forward_price / spot_price - 1.0) * 100.0

        # Contango: forward > spot
        contango_flag = forward_price > spot_price

        return {
            "status": "success",
            "gofo_pct": round(gofo_pct, 4),
            "lease_rate_pct": round(lease_rate_pct, 4),
            "forward_premium_pct": round(forward_premium_pct, 4),
            "contango_flag": contango_flag,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("precious_metals_lease_rate", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
