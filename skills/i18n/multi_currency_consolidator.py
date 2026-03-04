"""Consolidate multi-currency exposures into a base currency."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "multi_currency_consolidator",
    "description": "Converts positions into a base currency with exposure diagnostics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {"type": "array", "items": {"type": "object"}},
            "fx_rates": {"type": "object"},
            "base_currency": {"type": "string", "default": "USD"},
        },
        "required": ["positions", "fx_rates"],
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


def multi_currency_consolidator(
    positions: list[dict[str, Any]],
    fx_rates: dict[str, float],
    base_currency: str = "USD",
    **_: Any,
) -> dict[str, Any]:
    """Convert each position to the base currency and summarize exposure."""
    try:
        if not positions:
            raise ValueError("positions cannot be empty")
        base_currency = base_currency.upper()
        consolidated = []
        exposure: dict[str, float] = {}
        total_base = 0.0
        fx_rates_upper = {code.upper(): rate for code, rate in fx_rates.items()}
        fx_rates_upper.setdefault(base_currency, 1.0)

        for position in positions:
            currency = position.get("currency", base_currency).upper()
            rate = fx_rates_upper.get(currency)
            if rate is None or rate <= 0:
                raise ValueError(f"Missing FX rate for {currency}")
            amount = float(position.get("amount", 0))
            base_amount = amount * rate
            exposure[currency] = exposure.get(currency, 0.0) + base_amount
            total_base += base_amount
            consolidated.append(
                {
                    "asset": position.get("asset"),
                    "currency": currency,
                    "amount": amount,
                    "base_amount": round(base_amount, 2),
                }
            )

        non_base_exposure = {k: v for k, v in exposure.items() if k != base_currency}
        largest_risk = max(non_base_exposure, key=lambda cur: abs(non_base_exposure[cur]), default=base_currency)
        data = {
            "consolidated_positions": consolidated,
            "total_base_currency": round(total_base, 2),
            "currency_exposure": {k: round(v, 2) for k, v in exposure.items()},
            "largest_fx_risk": largest_risk,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("multi_currency_consolidator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
