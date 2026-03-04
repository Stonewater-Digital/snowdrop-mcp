"""
Executive Summary: Credit VaR using CreditMetrics/Vasicek formulation with obligor PDs, LGDs, and asset correlations.
Inputs: obligor_ratings (list[str]), transition_matrix (dict), exposures (list[float]), lgd_pct (list[float]), asset_correlations (list[float]), confidence_level (float)
Outputs: credit_var (float), expected_loss (float), unexpected_loss (float), contributions (list[dict])
MCP Tool Name: credit_var_calculator
"""
import logging
from datetime import datetime, timezone
from statistics import NormalDist
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_var_calculator",
    "description": "CreditMetrics style credit VaR computing conditional default probabilities and obligor contributions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "obligor_ratings": {
                "type": "array",
                "description": "List of current ratings (e.g., AAA, BBB, Default) for each obligor.",
                "items": {"type": "string"},
            },
            "transition_matrix": {
                "type": "object",
                "description": "Mapping of rating to probabilities of transitioning to other ratings including 'Default'.",
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "number",
                        "description": "Transition probability",
                    },
                    "description": "Row of transition probabilities",
                },
            },
            "exposures": {
                "type": "array",
                "description": "Exposure at default (EAD) for each obligor in base currency.",
                "items": {"type": "number"},
            },
            "lgd_pct": {
                "type": "array",
                "description": "Loss-given-default percentages per obligor (0-100).",
                "items": {"type": "number"},
            },
            "asset_correlations": {
                "type": "array",
                "description": "Asset correlations (rho) for each obligor vs systematic factor per Basel IRB guidance.",
                "items": {"type": "number"},
            },
            "confidence_level": {
                "type": "number",
                "description": "Confidence level for quantile, default 0.999 for credit portfolios.",
                "default": 0.999,
            },
        },
        "required": ["obligor_ratings", "transition_matrix", "exposures", "lgd_pct", "asset_correlations"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "credit VaR outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def credit_var_calculator(
    obligor_ratings: List[str],
    transition_matrix: Dict[str, Dict[str, float]],
    exposures: List[float],
    lgd_pct: List[float],
    asset_correlations: List[float],
    confidence_level: float = 0.999,
    **_: Any,
) -> dict[str, Any]:
    try:
        n = len(obligor_ratings)
        if not n:
            raise ValueError("obligor_ratings required")
        if not (len(exposures) == len(lgd_pct) == len(asset_correlations) == n):
            raise ValueError("input vectors must be same length")
        if not 0.5 < confidence_level < 1:
            raise ValueError("confidence_level must be between 0.5 and 1")

        inv_cdf = NormalDist().inv_cdf
        dist = NormalDist()
        z = inv_cdf(confidence_level)

        expected_loss = 0.0
        quantile_loss = 0.0
        contributions = []
        for idx in range(n):
            rating = obligor_ratings[idx]
            row = transition_matrix.get(rating)
            if not row:
                raise ValueError(f"missing transition row for rating {rating}")
            pd = float(row.get("Default", 0.0))
            rho = min(max(asset_correlations[idx], 0.0), 0.9999)
            lgd = lgd_pct[idx] / 100.0
            exposure = exposures[idx]

            expected_loss_i = exposure * lgd * pd
            expected_loss += expected_loss_i

            if pd <= 0:
                conditional_pd = 0.0
            elif pd >= 1:
                conditional_pd = 1.0
            else:
                conditional_pd = dist.cdf((inv_cdf(pd) + (rho ** 0.5) * z) / ((1 - rho) ** 0.5))
            quantile_loss_i = exposure * lgd * conditional_pd
            quantile_loss += quantile_loss_i
            contributions.append(
                {
                    "obligor_index": idx,
                    "pd": round(pd, 6),
                    "conditional_pd": round(conditional_pd, 6),
                    "expected_loss": round(expected_loss_i, 2),
                    "quantile_loss": round(quantile_loss_i, 2),
                    "rho": round(rho, 4),
                }
            )

        credit_var = quantile_loss - expected_loss
        data = {
            "credit_var": round(max(credit_var, 0.0), 2),
            "expected_loss": round(expected_loss, 2),
            "unexpected_loss": round(max(quantile_loss - expected_loss, 0.0), 2),
            "quantile_loss": round(quantile_loss, 2),
            "confidence_level": confidence_level,
            "z_score": round(z, 4),
            "contributions": contributions,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"credit_var_calculator failed: {e}")
        _log_lesson(f"credit_var_calculator: {e}")
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
