"""
Executive Summary: Climate transition risk capital impact modeling using sector exposures and scenario PD stresses.
Inputs: portfolio_sector_exposures (list[dict]), transition_scenario (str)
Outputs: stressed_pd_shifts (list[dict]), rwa_impact (float), stranded_asset_exposure (float)
MCP Tool Name: climate_risk_transition
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "climate_risk_transition",
    "description": "Applies NGFS transition scenarios to sector PDs and estimates RWA impact and stranded assets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_sector_exposures": {
                "type": "array",
                "description": "Sector exposures with base PD, LGD, and carbon intensity (tons CO2e/USDm).",
                "items": {
                    "type": "object",
                    "properties": {
                        "sector": {"type": "string", "description": "Sector name"},
                        "exposure": {"type": "number", "description": "Exposure amount"},
                        "base_pd": {"type": "number", "description": "Base PD in decimal"},
                        "lgd_pct": {"type": "number", "description": "LGD percentage"},
                        "carbon_intensity": {"type": "number", "description": "Carbon intensity metric"},
                    },
                    "required": ["sector", "exposure", "base_pd", "lgd_pct", "carbon_intensity"],
                },
            },
            "transition_scenario": {
                "type": "string",
                "description": "Scenario label (orderly, disorderly, hothouse).",
                "enum": ["orderly", "disorderly", "hothouse"],
            },
        },
        "required": ["portfolio_sector_exposures", "transition_scenario"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Climate transition metrics"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}

SCENARIO_MULTIPLIERS = {
    "orderly": 0.1,
    "disorderly": 0.3,
    "hothouse": 0.5,
}


def climate_risk_transition(
    portfolio_sector_exposures: List[Dict[str, Any]],
    transition_scenario: str,
    **_: Any,
) -> dict[str, Any]:
    try:
        if transition_scenario not in SCENARIO_MULTIPLIERS:
            raise ValueError("Unsupported transition scenario")
        multiplier = SCENARIO_MULTIPLIERS[transition_scenario]
        stressed = []
        base_rwa = stressed_rwa = 0.0
        stranded = 0.0
        for entry in portfolio_sector_exposures:
            exposure = entry["exposure"]
            pd_base = entry["base_pd"]
            intensity = entry["carbon_intensity"]
            lgd = entry["lgd_pct"] / 100.0
            pd_stress = min(pd_base * (1 + multiplier * (intensity / 100)), 1.0)
            base_loss = exposure * lgd * pd_base
            stress_loss = exposure * lgd * pd_stress
            base_rwa += base_loss * 12.5
            stressed_rwa += stress_loss * 12.5
            if intensity > 300:
                stranded += exposure * multiplier
            stressed.append(
                {
                    "sector": entry["sector"],
                    "base_pd": round(pd_base, 4),
                    "stressed_pd": round(pd_stress, 4),
                    "pd_shift_bps": round((pd_stress - pd_base) * 10000, 2),
                    "rwa_impact": round((stress_loss - base_loss) * 12.5, 2),
                }
            )
        data = {
            "stressed_pd_shifts": stressed,
            "rwa_impact": round(stressed_rwa - base_rwa, 2),
            "stranded_asset_exposure": round(stranded, 2),
            "scenario": transition_scenario,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"climate_risk_transition failed: {e}")
        _log_lesson(f"climate_risk_transition: {e}")
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
