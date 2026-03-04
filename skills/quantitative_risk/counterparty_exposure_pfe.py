"""
Executive Summary: Potential future exposure profiling consistent with Basel counterparty credit risk guidances.
Inputs: trade_mtm_series (list[dict]), netting_set (str), collateral (dict), margin_period_of_risk (int)
Outputs: pfe_profile (list[dict]), expected_exposure (float), effective_epe (float), collateral_buffer (float)
MCP Tool Name: counterparty_exposure_pfe
"""
import logging
from datetime import datetime, timezone
from statistics import NormalDist
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "counterparty_exposure_pfe",
    "description": "Computes potential future exposure (PFE) across tenors using collateralized netting set information.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "trade_mtm_series": {
                "type": "array",
                "description": "List of MTM scenario sets per tenor with mtm_values array.",
                "items": {
                    "type": "object",
                    "properties": {
                        "tenor_days": {"type": "integer", "description": "Tenor in days"},
                        "mtm_values": {
                            "type": "array",
                            "description": "Scenario MTMs (positive=receivable).",
                            "items": {"type": "number"},
                        },
                    },
                    "required": ["tenor_days", "mtm_values"],
                },
            },
            "netting_set": {
                "type": "string",
                "description": "Identifier of the counterparty netting set.",
            },
            "collateral": {
                "type": "object",
                "description": "Collateral terms including initial/variation margin and thresholds.",
                "properties": {
                    "initial_margin": {"type": "number", "description": "Posted initial margin"},
                    "variation_margin": {"type": "number", "description": "Current VM balance"},
                    "threshold": {"type": "number", "description": "CSA unsecured threshold"},
                },
                "required": ["initial_margin", "variation_margin", "threshold"],
            },
            "margin_period_of_risk": {
                "type": "integer",
                "description": "Margin period of risk in days for regulatory EAD.",
            },
            "confidence_level": {
                "type": "number",
                "description": "PFE percentile (default 0.975 as in IMM).",
                "default": 0.975,
            },
        },
        "required": ["trade_mtm_series", "netting_set", "collateral", "margin_period_of_risk"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "PFE outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def counterparty_exposure_pfe(
    trade_mtm_series: List[Dict[str, Any]],
    netting_set: str,
    collateral: Dict[str, float],
    margin_period_of_risk: int,
    confidence_level: float = 0.975,
    **_: Any,
) -> dict[str, Any]:
    try:
        if margin_period_of_risk <= 0:
            raise ValueError("margin_period_of_risk must be positive")
        if not trade_mtm_series:
            raise ValueError("trade_mtm_series required")
        if not 0.5 < confidence_level < 1:
            raise ValueError("confidence_level must be between 0.5 and 1")

        collateral_buffer = collateral["initial_margin"] + collateral["variation_margin"] - collateral["threshold"]
        percentile = NormalDist().inv_cdf(confidence_level)

        profile = []
        expected_exposure = 0.0
        weighted_sum = 0.0
        total_time = 0.0
        for tenor_entry in trade_mtm_series:
            tenor = tenor_entry["tenor_days"]
            scenarios = tenor_entry["mtm_values"]
            if not scenarios:
                raise ValueError("mtm_values must not be empty")
            adjusted = [max(value - collateral_buffer, 0.0) for value in scenarios]
            adjusted.sort()
            index = max(int(confidence_level * len(adjusted)) - 1, 0)
            pfe_value = adjusted[index]
            ee = sum(adjusted) / len(adjusted)
            profile.append(
                {
                    "tenor_days": tenor,
                    "pfe": round(pfe_value, 2),
                    "expected_exposure": round(ee, 2),
                }
            )
            expected_exposure += ee
            weighted_sum += ee * tenor
            total_time += tenor

        effective_epe = weighted_sum / total_time if total_time else expected_exposure
        data = {
            "netting_set": netting_set,
            "pfe_profile": profile,
            "confidence_level": confidence_level,
            "expected_exposure": round(expected_exposure / len(profile), 2),
            "effective_epe": round(effective_epe, 2),
            "collateral_buffer": round(collateral_buffer, 2),
            "margin_period_of_risk": margin_period_of_risk,
            "percentile_z": round(percentile, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"counterparty_exposure_pfe failed: {e}")
        _log_lesson(f"counterparty_exposure_pfe: {e}")
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
