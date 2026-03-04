"""
Executive Summary: ESG-screened mean-variance optimizer enforcing minimum score thresholds and sector caps.
Inputs: expected_returns (list[float]), covariance_matrix (list[list[float]]), esg_scores (list[float]), sector_labels (list[str]), min_esg_score (float)
Outputs: optimal_weights (list[float]), sector_allocation (list[dict]), portfolio_esg_score (float)
MCP Tool Name: esg_screened_optimizer
"""
import logging
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "esg_screened_optimizer",
    "description": (
        "Delivers a constrained mean-variance allocation subject to minimum ESG score, sector exclusions, and sector caps "
        "consistent with EU SFDR Article 8 screening."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "expected_returns": {
                "type": "array",
                "description": "Vector of expected returns per asset (decimal).",
                "items": {"type": "number"},
            },
            "covariance_matrix": {
                "type": "array",
                "description": "Covariance matrix for the same asset order.",
                "items": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
            "esg_scores": {
                "type": "array",
                "description": "Numeric ESG scores (0-100) for each asset.",
                "items": {"type": "number"},
            },
            "sector_labels": {
                "type": "array",
                "description": "GICS/NAICS sector tag for each asset.",
                "items": {"type": "string"},
            },
            "min_esg_score": {
                "type": "number",
                "description": "Minimum ESG score required (default 60).",
            },
            "excluded_sectors": {
                "type": "array",
                "description": "List of sector labels that are fully excluded.",
                "items": {"type": "string"},
            },
            "max_sector_weight": {
                "type": "number",
                "description": "Maximum percentage weight per sector (default 0.25).",
            },
            "risk_aversion": {
                "type": "number",
                "description": "Risk aversion parameter for mean-variance solution (default 3).",
            },
        },
        "required": ["expected_returns", "covariance_matrix", "esg_scores", "sector_labels"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Portfolio allocation"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def esg_screened_optimizer(
    expected_returns: List[float],
    covariance_matrix: List[List[float]],
    esg_scores: List[float],
    sector_labels: List[str],
    min_esg_score: float = 60.0,
    excluded_sectors: List[str] | None = None,
    max_sector_weight: float = 0.25,
    risk_aversion: float = 3.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        mu = np.asarray(expected_returns, dtype=float)
        cov = np.asarray(covariance_matrix, dtype=float)
        esg = np.asarray(esg_scores, dtype=float)
        sectors = list(sector_labels)
        if cov.shape[0] != cov.shape[1] or cov.shape[0] != mu.size:
            raise ValueError("Covariance dimension mismatch")
        if esg.size != mu.size or len(sectors) != mu.size:
            raise ValueError("ESG scores and sector labels must match asset count")
        mask = (esg >= min_esg_score)
        if excluded_sectors:
            excluded = set(excluded_sectors)
            mask &= np.array([sec not in excluded for sec in sectors])
        if not mask.any():
            raise ValueError("Screening removed all assets")
        idx = np.where(mask)[0]
        sub_mu = mu[idx]
        sub_cov = cov[np.ix_(idx, idx)]
        inv_cov = np.linalg.pinv(sub_cov)
        raw_weights = inv_cov @ sub_mu / risk_aversion
        raw_weights = np.maximum(raw_weights, 0.0)
        if raw_weights.sum() == 0:
            raw_weights = np.ones_like(raw_weights)
        raw_weights /= raw_weights.sum()
        eligible_weights = np.zeros(mu.size)
        eligible_weights[idx] = raw_weights
        sector_caps = defaultdict(float)
        for i, weight in enumerate(eligible_weights):
            sector = sectors[i]
            sector_caps[sector] += weight
        adjust_factor = 1.0
        for sector, weight in sector_caps.items():
            if weight > max_sector_weight:
                adjust_factor = min(adjust_factor, max_sector_weight / weight)
        if adjust_factor < 1.0:
            eligible_weights *= adjust_factor
            residual = 1 - eligible_weights.sum()
            if residual > 0:
                boost = eligible_weights > 0
                eligible_weights[boost] += residual / boost.sum()
        eligible_weights /= eligible_weights.sum()
        sector_allocation = defaultdict(float)
        weighted_esg = 0.0
        for weight, score, sector in zip(eligible_weights, esg, sectors):
            sector_allocation[sector] += weight
            weighted_esg += weight * score
        data = {
            "optimal_weights": eligible_weights.round(6).tolist(),
            "sector_allocation": [
                {"sector": sector, "weight": round(weight, 6)} for sector, weight in sector_allocation.items()
            ],
            "portfolio_esg_score": round(float(weighted_esg), 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, np.linalg.LinAlgError) as e:
        logger.error(f"esg_screened_optimizer failed: {e}")
        _log_lesson(f"esg_screened_optimizer: {e}")
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
