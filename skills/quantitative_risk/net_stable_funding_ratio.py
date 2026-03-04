"""
Executive Summary: Net Stable Funding Ratio as per Basel III Annex 2 using ASF and RSF weightings.
Inputs: available_stable_funding (list[dict]), required_stable_funding (list[dict])
Outputs: nsfr_ratio (float), asf_total (float), rsf_total (float), compliance (str)
MCP Tool Name: net_stable_funding_ratio
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "net_stable_funding_ratio",
    "description": "Calculates ASF and RSF weighted balances to determine NSFR compliance.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "available_stable_funding": {
                "type": "array",
                "description": "Items contributing to ASF with factors (0-100%).",
                "items": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number", "description": "Balance"},
                        "factor_pct": {"type": "number", "description": "ASF factor percentage"},
                        "category": {"type": "string", "description": "Narrative category"},
                    },
                    "required": ["amount", "factor_pct", "category"],
                },
            },
            "required_stable_funding": {
                "type": "array",
                "description": "Assets requiring funding with RSF factors (0-100%).",
                "items": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number", "description": "Asset balance"},
                        "factor_pct": {"type": "number", "description": "RSF factor"},
                        "category": {"type": "string", "description": "Category label"},
                    },
                    "required": ["amount", "factor_pct", "category"],
                },
            },
        },
        "required": ["available_stable_funding", "required_stable_funding"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "NSFR results"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _weighted_sum(items: List[dict[str, Any]]) -> float:
    total = 0.0
    for entry in items:
        factor = entry.get("factor_pct", 0.0) / 100.0
        total += entry.get("amount", 0.0) * factor
    return total


def net_stable_funding_ratio(
    available_stable_funding: List[dict[str, Any]],
    required_stable_funding: List[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    try:
        if not available_stable_funding or not required_stable_funding:
            raise ValueError("both ASF and RSF inputs required")
        asf_total = _weighted_sum(available_stable_funding)
        rsf_total = _weighted_sum(required_stable_funding)
        if rsf_total <= 0:
            raise ValueError("RSF total must be positive")
        nsfr_ratio = asf_total / rsf_total
        compliance = "compliant" if nsfr_ratio >= 1.0 else "breach"

        data = {
            "nsfr_ratio": round(nsfr_ratio * 100, 2),
            "asf_total": round(asf_total, 2),
            "rsf_total": round(rsf_total, 2),
            "compliance": compliance,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"net_stable_funding_ratio failed: {e}")
        _log_lesson(f"net_stable_funding_ratio: {e}")
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
