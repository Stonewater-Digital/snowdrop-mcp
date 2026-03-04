"""
Executive Summary: Basel IRRBB delta-EVE and delta-NII calculator using supervisory parallel and curve shocks.
Inputs: cashflows (list[dict]), yield_curve (dict[str,float]), shock_scenarios (dict[str,float])
Outputs: delta_eve (dict), delta_nii (dict), worst_scenario (str)
MCP Tool Name: interest_rate_risk_banking_book
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "interest_rate_risk_banking_book",
    "description": "Computes IRRBB delta EVE and NII across the six Basel shock scenarios.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cashflows": {
                "type": "array",
                "description": "Repricing buckets with cashflow amount and duration in years.",
                "items": {
                    "type": "object",
                    "properties": {
                        "bucket": {"type": "string", "description": "Time bucket label"},
                        "cashflow": {"type": "number", "description": "Cashflow amount"},
                        "duration_years": {"type": "number", "description": "Effective duration in years"},
                    },
                    "required": ["bucket", "cashflow", "duration_years"],
                },
            },
            "yield_curve": {
                "type": "object",
                "description": "Mapping of bucket names to base annual yields (decimal).",
                "additionalProperties": {"type": "number", "description": "Yield"},
            },
            "shock_scenarios": {
                "type": "object",
                "description": "Scenario name to parallel shock in basis points (per BCBS368).",
                "additionalProperties": {"type": "number", "description": "Shock in basis points"},
            },
        },
        "required": ["cashflows", "yield_curve", "shock_scenarios"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "IRRBB outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _present_value(cashflows: List[dict[str, Any]], levels: Dict[str, float]) -> float:
    pv = 0.0
    for entry in cashflows:
        bucket = entry["bucket"]
        rate = levels.get(bucket, 0.0)
        duration = entry["duration_years"]
        cashflow = entry["cashflow"]
        discount = (1 + rate) ** duration
        pv += cashflow / discount if discount else cashflow
    return pv


def interest_rate_risk_banking_book(
    cashflows: List[dict[str, Any]],
    yield_curve: Dict[str, float],
    shock_scenarios: Dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    try:
        if not cashflows:
            raise ValueError("cashflows required")
        base_pv = _present_value(cashflows, yield_curve)
        delta_eve = {}
        delta_nii = {}
        worst = None
        worst_value = 0.0
        for scenario, shock_bps in shock_scenarios.items():
            shocked_curve = {bucket: rate + shock_bps / 10000 for bucket, rate in yield_curve.items()}
            shocked_pv = _present_value(cashflows, shocked_curve)
            change = shocked_pv - base_pv
            delta_eve[scenario] = round(change, 2)
            rate_change = shock_bps / 10000
            nii_change = sum(entry["cashflow"] * rate_change * entry.get("duration_years", 1.0) for entry in cashflows)
            delta_nii[scenario] = round(nii_change, 2)
            if abs(change) > abs(worst_value):
                worst_value = change
                worst = scenario

        data = {
            "delta_eve": delta_eve,
            "delta_nii": delta_nii,
            "base_eve": round(base_pv, 2),
            "worst_scenario": worst,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"interest_rate_risk_banking_book failed: {e}")
        _log_lesson(f"interest_rate_risk_banking_book: {e}")
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
