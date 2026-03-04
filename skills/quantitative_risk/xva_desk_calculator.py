"""
Executive Summary: Aggregates CVA, DVA, FVA, KVA, and MVA using exposure curves and hazard rate approximations.
Inputs: exposure_profile (list[dict]), counterparty_pd (float), own_pd (float), funding_curve (list[dict]), capital_cost_pct (float), margin_profile (dict)
Outputs: cva (float), dva (float), fva (float), kva (float), mva (float), total_xva (float)
MCP Tool Name: xva_desk_calculator
"""
import logging
from datetime import datetime, timezone
from math import exp
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "xva_desk_calculator",
    "description": "Computes the suite of valuation adjustments using exposure profiles and hazard rate approximations.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposure_profile": {
                "type": "array",
                "description": "Expected exposure schedule by tenor in years.",
                "items": {
                    "type": "object",
                    "properties": {
                        "tenor_years": {"type": "number", "description": "Tenor in years"},
                        "expected_exposure": {"type": "number", "description": "Positive exposure"},
                    },
                    "required": ["tenor_years", "expected_exposure"],
                },
            },
            "counterparty_pd": {"type": "number", "description": "Annual counterparty PD (decimal)."},
            "own_pd": {"type": "number", "description": "Institution PD used for DVA (decimal)."},
            "funding_curve": {
                "type": "array",
                "description": "Discount factors represented by tenor and funding rate (decimal).",
                "items": {
                    "type": "object",
                    "properties": {
                        "tenor_years": {"type": "number", "description": "Tenor in years"},
                        "funding_rate_pct": {"type": "number", "description": "Funding rate %"},
                        "risk_free_rate_pct": {"type": "number", "description": "Risk free rate %"},
                    },
                    "required": ["tenor_years", "funding_rate_pct", "risk_free_rate_pct"],
                },
            },
            "capital_cost_pct": {"type": "number", "description": "Cost of capital used for KVA."},
            "margin_profile": {
                "type": "object",
                "description": "Margin terms (initial/variation).",
                "properties": {
                    "initial_margin": {"type": "number", "description": "Initial margin posted"},
                    "variation_margin": {"type": "number", "description": "Variation margin balance"},
                },
                "required": ["initial_margin", "variation_margin"],
            },
            "lgd_pct": {
                "type": "number",
                "description": "Loss-given-default percentage for CVA/DVA.",
                "default": 60.0,
            },
        },
        "required": [
            "exposure_profile",
            "counterparty_pd",
            "own_pd",
            "funding_curve",
            "capital_cost_pct",
            "margin_profile",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "XVA components"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _discount(rate_pct: float, tenor: float) -> float:
    return exp(-(rate_pct / 100.0) * tenor)


def xva_desk_calculator(
    exposure_profile: List[Dict[str, float]],
    counterparty_pd: float,
    own_pd: float,
    funding_curve: List[Dict[str, float]],
    capital_cost_pct: float,
    margin_profile: Dict[str, float],
    lgd_pct: float = 60.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not exposure_profile:
            raise ValueError("exposure_profile required")
        sorted_profile = sorted(exposure_profile, key=lambda x: x["tenor_years"])
        sorted_curve = sorted(funding_curve, key=lambda x: x["tenor_years"])
        lgd = lgd_pct / 100.0

        def incremental_pd(pd: float, dt: float) -> float:
            return 1 - exp(-pd * dt)

        cva = dva = fva = kva = 0.0
        prev_t = 0.0
        for exposure in sorted_profile:
            tenor = exposure["tenor_years"]
            ee = exposure["expected_exposure"]
            dt = max(tenor - prev_t, 0.0)
            discount_rate = next((item for item in sorted_curve if item["tenor_years"] >= tenor), sorted_curve[-1])
            df = _discount(discount_rate["risk_free_rate_pct"], tenor)
            cva += ee * lgd * incremental_pd(counterparty_pd, dt) * df
            dva += ee * lgd * incremental_pd(own_pd, dt) * df
            funding_spread = (discount_rate["funding_rate_pct"] - discount_rate["risk_free_rate_pct"]) / 100.0
            fva += ee * funding_spread * dt * df
            kva += ee * (capital_cost_pct / 100.0) * dt * df
            prev_t = tenor

        mva = margin_profile["initial_margin"] * (capital_cost_pct / 100.0)
        total = cva - dva + fva + kva + mva
        data = {
            "cva": round(cva, 2),
            "dva": round(dva, 2),
            "fva": round(fva, 2),
            "kva": round(kva, 2),
            "mva": round(mva, 2),
            "total_xva": round(total, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"xva_desk_calculator failed: {e}")
        _log_lesson(f"xva_desk_calculator: {e}")
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
