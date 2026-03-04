"""Summarize commodity term structure into level/slope/curvature."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "commodity_term_structure_model",
    "description": (
        "Fits an OLS linear regression to a commodity futures curve to estimate "
        "level (intercept at T=0), slope (price change per month), curvature (MSE of fit), "
        "and reports curve structure classification."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "futures_curve": {
                "type": "array",
                "description": "Futures curve points.",
                "items": {
                    "type": "object",
                    "properties": {
                        "tenor_months": {
                            "type": "number",
                            "description": "Months to contract expiry (must be > 0).",
                        },
                        "price": {
                            "type": "number",
                            "description": "Futures price at this tenor (must be > 0).",
                        },
                    },
                    "required": ["tenor_months", "price"],
                },
                "minItems": 3,
            }
        },
        "required": ["futures_curve"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "level": {"type": "number"},
            "slope_per_month": {"type": "number"},
            "curvature_mse": {"type": "number"},
            "r_squared": {"type": "number"},
            "structure": {"type": "string"},
            "timestamp": {"type": "string"},
        },
    },
}


def commodity_term_structure_model(
    futures_curve: Iterable[dict[str, float]],
    **_: Any,
) -> dict[str, Any]:
    """Return OLS level/slope/curvature fit to the futures term structure.

    Args:
        futures_curve: Iterable of dicts with ``tenor_months`` (> 0) and ``price`` (> 0).
            Minimum 3 points required for a meaningful fit.

    Returns:
        dict with status, level (OLS intercept), slope_per_month (OLS slope),
        curvature_mse (mean squared residual), r_squared (goodness of fit),
        and structure classification.

    Method:
        OLS linear regression: price = level + slope * tenor_months
        Solved analytically:
            slope = Σ[(t - t̄)(p - p̄)] / Σ[(t - t̄)²]
            level = p̄ - slope * t̄
        R² = 1 - SS_res / SS_tot where SS_tot = Σ(p - p̄)²

    Structure:
        upward slope > 0 (contango-consistent),
        downward slope < 0 (backwardation-consistent),
        flat if |slope| < 0.01% of mean price per month.
    """
    try:
        points = sorted(futures_curve, key=lambda item: float(item["tenor_months"]))
        if len(points) < 3:
            raise ValueError("Need at least three curve points for OLS fit")
        for i, p in enumerate(points):
            if float(p["tenor_months"]) <= 0:
                raise ValueError(f"futures_curve[{i}].tenor_months must be > 0")
            if float(p["price"]) <= 0:
                raise ValueError(f"futures_curve[{i}].price must be > 0")

        n = len(points)
        tenors = [float(p["tenor_months"]) for p in points]
        prices = [float(p["price"]) for p in points]

        mean_t = sum(tenors) / n
        mean_p = sum(prices) / n

        # OLS slope and intercept
        slope_num = sum((tenors[i] - mean_t) * (prices[i] - mean_p) for i in range(n))
        slope_den = sum((tenors[i] - mean_t) ** 2 for i in range(n))
        slope = slope_num / slope_den if slope_den != 0.0 else 0.0
        level = mean_p - slope * mean_t

        # Residuals and fit quality
        residuals = [prices[i] - (level + slope * tenors[i]) for i in range(n)]
        ss_res = sum(r ** 2 for r in residuals)
        ss_tot = sum((prices[i] - mean_p) ** 2 for i in range(n))
        mse = ss_res / n
        r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0

        # Flat threshold: |slope| < 0.01% of mean price per month
        flat_threshold = mean_p * 0.0001
        if slope > flat_threshold:
            structure = "upward"
        elif slope < -flat_threshold:
            structure = "downward"
        else:
            structure = "flat"

        return {
            "status": "success",
            "level": round(level, 4),
            "slope_per_month": round(slope, 6),
            "curvature_mse": round(mse, 4),
            "r_squared": round(r_squared, 4),
            "structure": structure,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("commodity_term_structure_model", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
