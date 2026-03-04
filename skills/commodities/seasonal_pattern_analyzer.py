"""Analyze seasonal price patterns for commodities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "seasonal_pattern_analyzer",
    "description": (
        "Aggregates historical commodity prices by calendar month to estimate seasonal factors, "
        "identify peak and trough months, and compute seasonal amplitude."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_prices": {
                "type": "array",
                "description": "Historical price observations with month labels.",
                "items": {
                    "type": "object",
                    "properties": {
                        "month": {
                            "type": "integer",
                            "description": "Calendar month (1–12).",
                        },
                        "price": {
                            "type": "number",
                            "description": "Price observation (must be > 0).",
                        },
                    },
                    "required": ["month", "price"],
                },
                "minItems": 12,
            }
        },
        "required": ["monthly_prices"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "seasonal_bias": {
                "type": "object",
                "description": "Month number -> fractional deviation from overall average (0 = neutral).",
            },
            "monthly_avg_prices": {
                "type": "object",
                "description": "Month number -> average price.",
            },
            "peak_month": {"type": "integer"},
            "trough_month": {"type": "integer"},
            "amplitude_pct": {"type": "number"},
            "months_covered": {"type": "integer"},
            "timestamp": {"type": "string"},
        },
    },
}


def seasonal_pattern_analyzer(
    monthly_prices: Iterable[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return normalized seasonal factors and bias flags.

    Args:
        monthly_prices: Iterable of dicts with ``month`` (1–12) and ``price`` (> 0) keys.
            At least 12 entries needed for one complete cycle.

    Returns:
        dict with status, seasonal_bias (fractional deviation from overall mean per month),
        monthly_avg_prices, peak_month, trough_month, amplitude_pct, months_covered.

    Seasonal bias:
        monthly_avg[m] = mean of all prices in month m
        overall_avg    = mean of all monthly_avg values (equal weight across months)
        seasonal_bias[m] = monthly_avg[m] / overall_avg - 1

    Amplitude: (peak_bias - trough_bias) * 100 in percentage points.
    """
    try:
        buckets: dict[int, list[float]] = {}
        for entry in monthly_prices:
            month = int(entry["month"])
            price = float(entry["price"])
            if month < 1 or month > 12:
                raise ValueError(f"month must be 1–12, got {month}")
            if price <= 0:
                raise ValueError(f"price must be positive, got {price}")
            buckets.setdefault(month, []).append(price)

        if not buckets:
            raise ValueError("No monthly price data provided")
        if len(buckets) < 2:
            raise ValueError("Need data for at least 2 different months")

        monthly_avg: dict[int, float] = {
            month: sum(values) / len(values) for month, values in buckets.items()
        }
        overall_avg = sum(monthly_avg.values()) / len(monthly_avg)
        if overall_avg <= 0:
            raise ValueError("Overall average price must be positive")

        seasonal_bias: dict[str, float] = {
            str(month): round(avg / overall_avg - 1.0, 4)
            for month, avg in sorted(monthly_avg.items())
        }
        monthly_avg_out: dict[str, float] = {
            str(month): round(avg, 4) for month, avg in sorted(monthly_avg.items())
        }

        peak = max(seasonal_bias.items(), key=lambda item: item[1])
        trough = min(seasonal_bias.items(), key=lambda item: item[1])
        amplitude_pct = (peak[1] - trough[1]) * 100.0

        return {
            "status": "success",
            "seasonal_bias": seasonal_bias,
            "monthly_avg_prices": monthly_avg_out,
            "peak_month": int(peak[0]),
            "trough_month": int(trough[0]),
            "amplitude_pct": round(amplitude_pct, 2),
            "months_covered": len(buckets),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("seasonal_pattern_analyzer", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
