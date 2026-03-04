"""
Executive Summary: IFRS 17 contractual service margin computation and release schedule.
Inputs: fulfillment_cashflows (list[dict]), risk_adjustment (float), premium_received (float), discount_rate_pct (float), coverage_units (list[float])
Outputs: initial_csm (float), csm_amortization (list[dict]), profit_recognition (float)
MCP Tool Name: ifrs17_csm_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ifrs17_csm_calculator",
    "description": "Calculates IFRS 17 contractual service margin and amortizes it over coverage units.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fulfillment_cashflows": {
                "type": "array",
                "description": "Expected future cashflows with timing in years.",
                "items": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "number", "description": "Year index"},
                        "cashflow": {"type": "number", "description": "Cashflow amount (positive inflow)"},
                    },
                    "required": ["year", "cashflow"],
                },
            },
            "risk_adjustment": {"type": "number", "description": "Risk adjustment amount."},
            "premium_received": {"type": "number", "description": "Premium received at inception."},
            "discount_rate_pct": {"type": "number", "description": "Discount rate for PV."},
            "coverage_units": {
                "type": "array",
                "description": "Coverage units per period for CSM release.",
                "items": {"type": "number"},
            },
        },
        "required": ["fulfillment_cashflows", "risk_adjustment", "premium_received", "discount_rate_pct", "coverage_units"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "CSM output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _discount(rate_pct: float, year: float) -> float:
    return 1 / ((1 + rate_pct / 100.0) ** year)


def ifrs17_csm_calculator(
    fulfillment_cashflows: List[Dict[str, float]],
    risk_adjustment: float,
    premium_received: float,
    discount_rate_pct: float,
    coverage_units: List[float],
    **_: Any,
) -> dict[str, Any]:
    try:
        if not fulfillment_cashflows or not coverage_units:
            raise ValueError("fulfillment_cashflows and coverage_units required")
        pv_cashflows = sum(cf["cashflow"] * _discount(discount_rate_pct, cf["year"]) for cf in fulfillment_cashflows)
        initial_csm = premium_received + risk_adjustment - pv_cashflows
        total_units = sum(coverage_units)
        amortization = []
        carrying_amount = initial_csm
        for period, units in enumerate(coverage_units, start=1):
            release = (initial_csm * (units / total_units)) if total_units else 0.0
            carrying_amount -= release
            amortization.append(
                {
                    "period": period,
                    "coverage_units": units,
                    "csm_release": round(release, 2),
                    "remaining_csm": round(max(carrying_amount, 0.0), 2),
                }
            )
        data = {
            "initial_csm": round(initial_csm, 2),
            "csm_amortization": amortization,
            "profit_recognition": round(sum(item["csm_release"] for item in amortization), 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ifrs17_csm_calculator failed: {e}")
        _log_lesson(f"ifrs17_csm_calculator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
