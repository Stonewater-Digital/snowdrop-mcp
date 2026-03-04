"""Mark a multi-currency portfolio to base currency."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "market_value_calculator",
    "description": "Converts multi-currency positions to a base currency and aggregates exposure.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {"type": "array", "items": {"type": "object"}},
            "fx_rates": {"type": "object"},
            "base_currency": {"type": "string"},
        },
        "required": ["positions", "fx_rates", "base_currency"],
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


def market_value_calculator(
    positions: list[dict[str, Any]],
    fx_rates: dict[str, float],
    base_currency: str,
    **_: Any,
) -> dict[str, Any]:
    """Return total market value and currency exposure."""
    try:
        total_value = 0.0
        currency_exposure: dict[str, float] = {}
        breakdown: list[dict[str, Any]] = []
        for position in positions or []:
            currency = str(position.get("currency", base_currency)).upper()
            rate = fx_rates.get(currency)
            if rate is None and currency != base_currency:
                raise ValueError(f"Missing FX rate for {currency}")
            local_value = float(position.get("quantity", 0.0)) * float(position.get("local_price", 0.0))
            converted = local_value if currency == base_currency else local_value * rate
            currency_exposure[currency] = currency_exposure.get(currency, 0.0) + converted
            total_value += converted
            breakdown.append(
                {
                    "security_id": position.get("security_id"),
                    "currency": currency,
                    "local_value": round(local_value, 2),
                    "converted_value": round(converted, 2),
                }
            )
        data = {
            "base_currency": base_currency.upper(),
            "total_market_value_base": round(total_value, 2),
            "position_breakdown": breakdown,
            "currency_exposure": {k: round(v, 2) for k, v in currency_exposure.items()},
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] market_value_calculator: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
