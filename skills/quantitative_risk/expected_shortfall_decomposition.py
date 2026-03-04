"""
Executive Summary: Expected shortfall decomposition attributing tail risk to systematic factors per Basel ES methodology.
Inputs: portfolio_pnl (list[float]), factor_exposures (dict[str,float]), factor_returns (dict[str,list[float]]), confidence_level (float)
Outputs: total_expected_shortfall (float), factor_contributions (list[dict]), concentration_ratio (float)
MCP Tool Name: expected_shortfall_decomposition
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "expected_shortfall_decomposition",
    "description": "Basel III ES attribution by computing conditional tail expectations and factor contributions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_pnl": {
                "type": "array",
                "description": "Historical or simulated P&L series in base currency.",
                "items": {"type": "number"},
            },
            "factor_exposures": {
                "type": "object",
                "description": "Factor betas or sensitivities keyed by factor name.",
                "additionalProperties": {"type": "number", "description": "Sensitivity to the factor"},
            },
            "factor_returns": {
                "type": "object",
                "description": "Dictionary of factor return series aligned with portfolio P&L observations.",
                "additionalProperties": {
                    "type": "array",
                    "description": "Return series for a factor",
                    "items": {"type": "number", "description": "Factor return"},
                },
            },
            "confidence_level": {
                "type": "number",
                "description": "Tail probability threshold (default 0.975 as per FRTB).",
                "default": 0.975,
            },
        },
        "required": ["portfolio_pnl", "factor_exposures", "factor_returns"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status value"},
            "data": {"type": "object", "description": "ES attribution"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def expected_shortfall_decomposition(
    portfolio_pnl: List[float],
    factor_exposures: Dict[str, float],
    factor_returns: Dict[str, List[float]],
    confidence_level: float = 0.975,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not portfolio_pnl:
            raise ValueError("portfolio_pnl required")
        if not 0.5 < confidence_level < 1:
            raise ValueError("confidence_level must be between 0.5 and 1")
        num_obs = len(portfolio_pnl)
        for series in factor_returns.values():
            if len(series) != num_obs:
                raise ValueError("factor return lengths must match portfolio_pnl length")

        losses = [-value for value in portfolio_pnl]
        sorted_indices = sorted(range(num_obs), key=lambda idx: losses[idx])
        cutoff_index = int(confidence_level * num_obs)
        cutoff_index = min(max(cutoff_index, 1), num_obs)
        tail_indices = sorted_indices[cutoff_index - 1 :]
        if not tail_indices:
            tail_indices = sorted_indices[-1:]
        total_es = sum(losses[idx] for idx in tail_indices) / len(tail_indices)

        factor_contributions = []
        concentration_total = 0.0
        for factor, beta in factor_exposures.items():
            series = factor_returns.get(factor)
            if series is None:
                continue
            tail_effect = sum(-beta * series[idx] for idx in tail_indices) / len(tail_indices)
            contribution_pct = tail_effect / total_es if total_es else 0.0
            concentration_total += contribution_pct ** 2
            factor_contributions.append(
                {
                    "factor": factor,
                    "beta": beta,
                    "tail_loss_contribution": round(tail_effect, 6),
                    "percentage_of_es": round(contribution_pct * 100, 4),
                }
            )

        concentration_ratio = concentration_total ** 0.5
        data = {
            "total_expected_shortfall": round(total_es, 6),
            "factor_contributions": factor_contributions,
            "concentration_ratio": round(concentration_ratio, 6),
            "confidence_level": confidence_level,
            "tail_count": len(tail_indices),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"expected_shortfall_decomposition failed: {e}")
        _log_lesson(f"expected_shortfall_decomposition: {e}")
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
