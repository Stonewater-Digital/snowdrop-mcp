"""
Executive Summary: Portable alpha constructor fusing active alpha sleeves with a futures overlay to retain beta exposure.
Inputs: alpha_sleeves (list[dict]), beta_index (dict), futures_spec (dict)
Outputs: allocation_plan (list[dict]), overlay_notional (float), expected_tracking_error (float), blended_return (float)
MCP Tool Name: portable_alpha_constructor
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "portable_alpha_constructor",
    "description": (
        "Combines capital allocations to uncorrelated alpha sleeves with a futures overlay sized to target beta "
        "exposure, following the portable alpha framework used by Canadian pensions."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "alpha_sleeves": {
                "type": "array",
                "description": "List of alpha sleeves including capital percentage and expected stats.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Sleeve identifier"},
                        "capital_pct": {"type": "number", "description": "Capital share allocated (0-1)."},
                        "expected_return": {"type": "number", "description": "Annualized expected return (decimal)."},
                        "volatility": {"type": "number", "description": "Annualized volatility (decimal)."},
                        "correlation_to_beta": {"type": "number", "description": "Correlation to beta benchmark."},
                    },
                    "required": ["name", "capital_pct", "expected_return", "volatility", "correlation_to_beta"],
                },
            },
            "beta_index": {
                "type": "object",
                "description": "Benchmark beta exposure stats (return, volatility).",
                "properties": {
                    "expected_return": {"type": "number", "description": "Benchmark annual return"},
                    "volatility": {"type": "number", "description": "Benchmark annual volatility"},
                    "target_beta": {"type": "number", "description": "Desired beta exposure (typically 1)."},
                },
                "required": ["expected_return", "volatility", "target_beta"],
            },
            "futures_spec": {
                "type": "object",
                "description": "Overlay futures specification (price, contract multiplier).",
                "properties": {
                    "contract_price": {"type": "number", "description": "Current futures price"},
                    "multiplier": {"type": "number", "description": "Dollar value per index point."},
                    "portfolio_value": {"type": "number", "description": "Total portfolio value (base currency)."},
                },
                "required": ["contract_price", "multiplier", "portfolio_value"],
            },
        },
        "required": ["alpha_sleeves", "beta_index", "futures_spec"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Portable alpha allocation"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def portable_alpha_constructor(
    alpha_sleeves: List[Dict[str, Any]],
    beta_index: Dict[str, float],
    futures_spec: Dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    try:
        if not alpha_sleeves:
            raise ValueError("alpha_sleeves cannot be empty")
        capital_total = sum(sleeve["capital_pct"] for sleeve in alpha_sleeves)
        if capital_total > 1.0 + 1e-6:
            raise ValueError("Alpha capital percentages cannot exceed 100%")
        portfolio_value = float(futures_spec["portfolio_value"])
        target_beta = float(beta_index["target_beta"])
        multiplier = float(futures_spec["multiplier"])
        contract_price = float(futures_spec["contract_price"])
        overlay_notional = portfolio_value * target_beta
        contracts = overlay_notional / (contract_price * multiplier)
        blended_return = 0.0
        blended_var = (target_beta * beta_index["volatility"]) ** 2
        allocation_plan = []
        for sleeve in alpha_sleeves:
            weight = sleeve["capital_pct"]
            exp_return = sleeve["expected_return"]
            vol = sleeve["volatility"]
            corr = sleeve["correlation_to_beta"]
            blended_return += weight * exp_return
            alpha_var = (weight * vol) ** 2
            covariance = 2 * weight * vol * target_beta * beta_index["volatility"] * corr
            blended_var += alpha_var + covariance
            allocation_plan.append(
                {
                    "sleeve": sleeve["name"],
                    "capital_pct": weight,
                    "expected_return": exp_return,
                    "volatility": vol,
                }
            )
        blended_return += target_beta * beta_index["expected_return"]
        expected_tracking_error = max(0.0, blended_var) ** 0.5
        data = {
            "allocation_plan": allocation_plan,
            "overlay_notional": round(overlay_notional, 2),
            "contracts_required": round(contracts, 2),
            "blended_return": round(blended_return, 4),
            "expected_tracking_error": round(expected_tracking_error, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"portable_alpha_constructor failed: {e}")
        _log_lesson(f"portable_alpha_constructor: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as log_file:
            log_file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
