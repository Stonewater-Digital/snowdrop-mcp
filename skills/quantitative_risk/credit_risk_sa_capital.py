"""
Executive Summary: Basel III standardized credit risk capital calculation using exposure, CCF, and CRM adjustments.
Inputs: exposures (list[dict]), tier1_ratio_target (float)
Outputs: total_rwa (float), capital_requirement (float), average_risk_weight (float)
MCP Tool Name: credit_risk_sa_capital
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_risk_sa_capital",
    "description": "Calculates RWA for standardized approach exposures with credit conversion and collateral mitigation.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposures": {
                "type": "array",
                "description": "Exposure items with risk weight and credit conversion factors.",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Regulatory exposure class"},
                        "ead": {"type": "number", "description": "Exposure at default"},
                        "risk_weight_pct": {"type": "number", "description": "Risk weight percentage"},
                        "ccf_pct": {"type": "number", "description": "Credit conversion factor", "default": 100.0},
                        "collateral_value": {"type": "number", "description": "Recognized collateral"},
                    },
                    "required": ["category", "ead", "risk_weight_pct"],
                },
            },
            "capital_ratio_pct": {
                "type": "number",
                "description": "Regulatory capital ratio to apply (default 8%).",
                "default": 8.0,
            },
        },
        "required": ["exposures"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "RWA breakdown"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def credit_risk_sa_capital(
    exposures: List[dict[str, Any]],
    capital_ratio_pct: float = 8.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not exposures:
            raise ValueError("exposures required")
        total_rwa = 0.0
        total_ead = 0.0
        breakdown = []
        for entry in exposures:
            ead = entry.get("ead", 0.0)
            ccf = entry.get("ccf_pct", 100.0) / 100.0
            rw = entry.get("risk_weight_pct", 0.0) / 100.0
            collateral = entry.get("collateral_value", 0.0)
            effective_ead = max(ead * ccf - collateral, 0.0)
            rwa = effective_ead * rw
            total_rwa += rwa
            total_ead += ead
            breakdown.append(
                {
                    "category": entry.get("category"),
                    "effective_ead": round(effective_ead, 2),
                    "risk_weight_pct": entry.get("risk_weight_pct", 0.0),
                    "rwa": round(rwa, 2),
                }
            )
        capital_requirement = total_rwa * (capital_ratio_pct / 100.0)
        avg_rw = (total_rwa / total_ead) * 100 if total_ead else 0.0
        data = {
            "total_rwa": round(total_rwa, 2),
            "capital_requirement": round(capital_requirement, 2),
            "average_risk_weight_pct": round(avg_rw, 2),
            "breakdown": breakdown,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"credit_risk_sa_capital failed: {e}")
        _log_lesson(f"credit_risk_sa_capital: {e}")
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
