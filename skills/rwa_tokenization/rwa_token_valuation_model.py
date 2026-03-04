"""Value RWA tokens using discounted cash flow inputs.
Supports per-token pricing and sensitivity to discount rates."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_token_valuation_model",
    "description": "Discounts projected cash flows to derive intrinsic value per RWA token.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash_flows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "period_years": {"type": "number"},
                        "amount": {"type": "number"},
                    },
                    "required": ["period_years", "amount"],
                },
                "description": "Projected cash flows with timing in years.",
            },
            "discount_rate_pct": {"type": "number", "description": "Annual discount rate"},
            "token_supply": {"type": "number", "description": "Outstanding token count"},
        },
        "required": ["cash_flows", "discount_rate_pct", "token_supply"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def rwa_token_valuation_model(
    cash_flows: Sequence[dict[str, float]],
    discount_rate_pct: float,
    token_supply: float,
    **_: Any,
) -> dict[str, Any]:
    """Discount cash flows to price RWA tokens.

    Args:
        cash_flows: Sequence of projected distributions with timing in years.
        discount_rate_pct: Annual discount rate percent.
        token_supply: Tokens outstanding.

    Returns:
        Dict with net present value totals and per-token price.
    """
    try:
        if token_supply <= 0:
            raise ValueError("token_supply must be positive")
        discount_rate = discount_rate_pct / 100
        npv = 0.0
        discounted = []
        for flow in cash_flows:
            period = float(flow.get("period_years", 0))
            amount = float(flow.get("amount", 0))
            factor = (1 + discount_rate) ** period
            pv = amount / factor if factor else 0.0
            discounted.append({"period_years": period, "amount": amount, "present_value": round(pv, 2)})
            npv += pv
        price_per_token = npv / token_supply
        data = {
            "present_value": round(npv, 2),
            "price_per_token": round(price_per_token, 6),
            "discounted_cash_flows": discounted,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_token_valuation_model failure: %s", exc)
        log_lesson(f"rwa_token_valuation_model: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
