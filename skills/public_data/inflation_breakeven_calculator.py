"""Calculate inflation breakeven rate from nominal and TIPS yields.

MCP Tool Name: inflation_breakeven_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "inflation_breakeven_calculator",
    "description": "Calculate the inflation breakeven rate from nominal Treasury yield and TIPS yield. The breakeven rate represents market-implied inflation expectations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "nominal_yield": {
                "type": "number",
                "description": "Nominal Treasury yield as percentage (e.g., 4.25 for 4.25%).",
            },
            "tips_yield": {
                "type": "number",
                "description": "TIPS (Treasury Inflation-Protected Securities) yield as percentage (e.g., 1.95 for 1.95%).",
            },
        },
        "required": ["nominal_yield", "tips_yield"],
    },
}


def inflation_breakeven_calculator(
    nominal_yield: float,
    tips_yield: float,
) -> dict[str, Any]:
    """Calculate inflation breakeven rate from nominal and TIPS yields."""
    try:
        breakeven = nominal_yield - tips_yield

        if breakeven < 1.5:
            assessment = "Below-average inflation expectations. Markets expect very low inflation or potential deflation risk."
        elif breakeven < 2.0:
            assessment = "Below Fed target. Markets expect inflation below the Fed's 2% target."
        elif breakeven < 2.5:
            assessment = "Near Fed target. Markets expect inflation roughly in line with the Fed's 2% objective."
        elif breakeven < 3.0:
            assessment = "Above Fed target. Markets expect moderately elevated inflation."
        else:
            assessment = "Significantly above target. Markets are pricing in sustained above-target inflation."

        return {
            "status": "ok",
            "data": {
                "nominal_yield_pct": nominal_yield,
                "tips_yield_pct": tips_yield,
                "breakeven_rate_pct": round(breakeven, 4),
                "assessment": assessment,
                "interpretation": (
                    f"The breakeven inflation rate is {breakeven:.2f}%. This means TIPS outperform "
                    f"nominal Treasuries if realized inflation exceeds {breakeven:.2f}% over the bond's term. "
                    f"Conversely, nominal Treasuries outperform if inflation stays below {breakeven:.2f}%."
                ),
                "note": "The breakeven rate includes both inflation expectations and an inflation risk premium, "
                "so it may slightly overstate pure inflation expectations.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
