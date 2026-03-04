"""
Executive Summary: Fundamental Review of the Trading Book standardized approach capital calculator with correlation scenarios.
Inputs: sensitivities (list[dict]), correlation_scenarios (dict[str,float]), drc_addon (float)
Outputs: capital_by_risk_class (dict), aggregate_capital (float), scenario_breakdown (dict)
MCP Tool Name: market_risk_frtb_sa
"""
import logging
from datetime import datetime, timezone
from math import sqrt
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "market_risk_frtb_sa",
    "description": "Computes delta/vega/curvature buckets with prescribed correlations to derive FRTB SA capital plus DRC add-on.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sensitivities": {
                "type": "array",
                "description": "Per risk class sensitivities with Basel risk weights.",
                "items": {
                    "type": "object",
                    "properties": {
                        "risk_class": {"type": "string", "description": "Risk class label (IR, FX, EQ, etc.)"},
                        "delta": {"type": "number", "description": "Weighted delta sensitivity"},
                        "vega": {"type": "number", "description": "Weighted vega sensitivity"},
                        "curvature": {"type": "number", "description": "Curvature term"},
                        "risk_weight": {"type": "number", "description": "Risk weight multiplier"},
                    },
                    "required": ["risk_class", "delta", "vega", "curvature", "risk_weight"],
                },
            },
            "correlation_scenarios": {
                "type": "object",
                "description": "Correlation parameter rho for low/medium/high stress calibration.",
                "properties": {
                    "low": {"type": "number", "description": "Low correlation case"},
                    "medium": {"type": "number", "description": "Medium correlation case"},
                    "high": {"type": "number", "description": "High correlation case"},
                },
                "required": ["low", "medium", "high"],
            },
            "drc_addon": {
                "type": "number",
                "description": "Default risk capital add-on in base currency.",
                "default": 0.0,
            },
        },
        "required": ["sensitivities", "correlation_scenarios"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "FRTB outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def market_risk_frtb_sa(
    sensitivities: List[Dict[str, Any]],
    correlation_scenarios: Dict[str, float],
    drc_addon: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not sensitivities:
            raise ValueError("sensitivities required")
        scenario_capitals: Dict[str, Dict[str, float]] = {key: {} for key in correlation_scenarios}
        for entry in sensitivities:
            weight = entry["risk_weight"]
            delta = entry["delta"] * weight
            vega = entry["vega"] * weight
            curvature = entry["curvature"] * weight
            risk_class = entry["risk_class"]
            for scenario, rho in correlation_scenarios.items():
                corr = max(min(rho, 0.99), -0.99)
                capital = sqrt(
                    delta**2
                    + vega**2
                    + curvature**2
                    + 2 * corr * abs(delta * vega)
                    + 2 * corr * abs(delta * curvature)
                    + 2 * corr * abs(vega * curvature)
                )
                scenario_capitals[scenario][risk_class] = scenario_capitals[scenario].get(risk_class, 0.0) + capital

        aggregate = {}
        for scenario, charges in scenario_capitals.items():
            aggregate[scenario] = sum(charges.values()) + drc_addon

        worst_scenario = max(aggregate, key=aggregate.get)
        data = {
            "capital_by_risk_class": scenario_capitals[worst_scenario],
            "aggregate_capital": round(aggregate[worst_scenario], 2),
            "scenario_breakdown": {s: round(v, 2) for s, v in aggregate.items()},
            "drc_addon": round(drc_addon, 2),
            "worst_scenario": worst_scenario,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"market_risk_frtb_sa failed: {e}")
        _log_lesson(f"market_risk_frtb_sa: {e}")
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
