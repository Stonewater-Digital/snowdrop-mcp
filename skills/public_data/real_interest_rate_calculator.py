"""Calculate real interest rate using the Fisher equation.

MCP Tool Name: real_interest_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "real_interest_rate_calculator",
    "description": "Calculate the real interest rate from nominal rate and inflation using the Fisher equation. Returns both exact and approximate values.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "nominal_rate": {
                "type": "number",
                "description": "Nominal interest rate as a decimal (e.g., 0.05 for 5%).",
            },
            "inflation_rate": {
                "type": "number",
                "description": "Inflation rate as a decimal (e.g., 0.03 for 3%).",
            },
        },
        "required": ["nominal_rate", "inflation_rate"],
    },
}


def real_interest_rate_calculator(
    nominal_rate: float,
    inflation_rate: float,
) -> dict[str, Any]:
    """Calculate real interest rate using the Fisher equation."""
    try:
        if inflation_rate == -1.0:
            return {
                "status": "error",
                "data": {"error": "Inflation rate of -100% causes division by zero in Fisher equation."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Exact Fisher equation: (1 + r) = (1 + i) / (1 + π)
        exact_real = (1 + nominal_rate) / (1 + inflation_rate) - 1

        # Linear approximation: r ≈ i - π
        approx_real = nominal_rate - inflation_rate

        return {
            "status": "ok",
            "data": {
                "nominal_rate": nominal_rate,
                "nominal_rate_pct": round(nominal_rate * 100, 4),
                "inflation_rate": inflation_rate,
                "inflation_rate_pct": round(inflation_rate * 100, 4),
                "real_rate_exact": round(exact_real, 6),
                "real_rate_exact_pct": round(exact_real * 100, 4),
                "real_rate_approx": round(approx_real, 6),
                "real_rate_approx_pct": round(approx_real * 100, 4),
                "approximation_error_pct": round((exact_real - approx_real) * 100, 4),
                "interpretation": (
                    f"With a nominal rate of {nominal_rate*100:.2f}% and inflation of {inflation_rate*100:.2f}%, "
                    f"the real interest rate is {exact_real*100:.2f}% (Fisher exact). "
                    f"{'Positive real rate: savers earn returns above inflation.' if exact_real > 0 else 'Negative real rate: inflation erodes the value of savings faster than interest accumulates.'}"
                ),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
