"""
Executive Summary: Volcker Rule compliance checker for RENTD, inventory, and customer-facing metrics.
Inputs: trading_desk_inventory (float), rentd_limit (float), rentd_usage (float), customer_flow_ratio (float), risk_limit (float), value_at_risk (float)
Outputs: compliance_status (str), metric_breakdown (list[dict]), near_miss_flags (list[str])
MCP Tool Name: dodd_frank_volcker_compliance
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "dodd_frank_volcker_compliance",
    "description": "Evaluates RENTD, inventory, and VaR metrics against Volcker Rule limits.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "trading_desk_inventory": {"type": "number", "description": "Current inventory (positive=long)."},
            "rentd_limit": {"type": "number", "description": "Reasonably expected near term demand limit."},
            "rentd_usage": {"type": "number", "description": "Current RENTD usage."},
            "customer_flow_ratio": {"type": "number", "description": "Customer facing volumes / proprietary volumes."},
            "risk_limit": {"type": "number", "description": "Approved VaR limit."},
            "value_at_risk": {"type": "number", "description": "Current VaR metric."},
        },
        "required": [
            "trading_desk_inventory",
            "rentd_limit",
            "rentd_usage",
            "customer_flow_ratio",
            "risk_limit",
            "value_at_risk",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Compliance summary"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def dodd_frank_volcker_compliance(
    trading_desk_inventory: float,
    rentd_limit: float,
    rentd_usage: float,
    customer_flow_ratio: float,
    risk_limit: float,
    value_at_risk: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        metrics: List[dict[str, Any]] = []
        status_flags = []
        rentd_pct = rentd_usage / rentd_limit if rentd_limit else 0.0
        metrics.append({"metric": "RENTD", "usage_pct": round(rentd_pct * 100, 2), "limit": rentd_limit})
        if rentd_pct > 1:
            status_flags.append("RENTD breach")
        elif rentd_pct > 0.9:
            status_flags.append("RENTD near miss")

        customer_flag = customer_flow_ratio >= 0.75
        metrics.append({"metric": "Customer flow", "ratio": round(customer_flow_ratio, 2), "threshold": 0.75})
        if not customer_flag:
            status_flags.append("Insufficient customer volume")

        risk_pct = value_at_risk / risk_limit if risk_limit else 0.0
        metrics.append({"metric": "VaR", "usage_pct": round(risk_pct * 100, 2), "limit": risk_limit})
        if risk_pct > 1:
            status_flags.append("VaR limit breach")
        elif risk_pct > 0.95:
            status_flags.append("VaR near miss")

        inventory_ok = abs(trading_desk_inventory) <= rentd_limit
        metrics.append({"metric": "Inventory", "value": trading_desk_inventory, "limit": rentd_limit})
        if not inventory_ok:
            status_flags.append("Inventory exceeds RENTD")

        compliance_status = "breach" if any("breach" in flag.lower() for flag in status_flags) else "warning" if status_flags else "compliant"
        data = {
            "compliance_status": compliance_status,
            "metric_breakdown": metrics,
            "near_miss_flags": status_flags,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"dodd_frank_volcker_compliance failed: {e}")
        _log_lesson(f"dodd_frank_volcker_compliance: {e}")
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
