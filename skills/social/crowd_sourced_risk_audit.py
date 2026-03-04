"""
Executive Summary: Consensus aggregation engine for asset risk — confidence-weights individual assessor scores, detects statistical outliers, and reports overall consensus strength.
Inputs: asset_id (str), assessments (list[dict: assessor_id, risk_score (1-10), confidence (0-1), rationale (str)])
Outputs: consensus_risk_score (float), consensus_level (str), outlier_assessments (list), assessment_count (int)
MCP Tool Name: crowd_sourced_risk_audit
"""
import math
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "crowd_sourced_risk_audit",
    "description": "Aggregates multi-assessor risk scores into a confidence-weighted consensus, surfaces statistical outliers, and classifies overall consensus strength.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_id": {"type": "string", "description": "Identifier for the asset being audited."},
            "assessments": {
                "type": "array",
                "description": (
                    "List of assessment dicts with: assessor_id (str), "
                    "risk_score (float 1-10), confidence (float 0-1), rationale (str)."
                ),
                "items": {"type": "object"},
            },
        },
        "required": ["asset_id", "assessments"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "consensus_risk_score": {"type": "number"},
            "consensus_level": {"type": "string"},
            "outlier_assessments": {"type": "array"},
            "assessment_count": {"type": "integer"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": ["status", "timestamp"],
    },
}

# Thresholds for consensus classification
STRONG_STDDEV_THRESHOLD = 1.0
MODERATE_STDDEV_THRESHOLD = 2.0
# Outlier z-score threshold
OUTLIER_Z_THRESHOLD = 2.0
# Minimum confidence to include an assessment
MIN_CONFIDENCE = 0.0  # accept all, but zero-confidence gets no weight


def _weighted_stats(
    scores: list[float], weights: list[float]
) -> tuple[float, float]:
    """Calculate weighted mean and weighted standard deviation.

    Args:
        scores: Risk score values.
        weights: Corresponding confidence weights (must be same length).

    Returns:
        Tuple of (weighted_mean, weighted_stddev). Both are 0.0 if no weight.
    """
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0, 0.0

    mean = sum(s * w for s, w in zip(scores, weights)) / total_weight
    variance = (
        sum(w * (s - mean) ** 2 for s, w in zip(scores, weights)) / total_weight
    )
    return round(mean, 4), round(math.sqrt(variance), 4)


def _classify_consensus(stddev: float) -> str:
    """Map weighted standard deviation to a consensus level label.

    Args:
        stddev: Weighted standard deviation of risk scores.

    Returns:
        "strong", "moderate", or "weak".
    """
    if stddev <= STRONG_STDDEV_THRESHOLD:
        return "strong"
    if stddev <= MODERATE_STDDEV_THRESHOLD:
        return "moderate"
    return "weak"


def crowd_sourced_risk_audit(
    asset_id: str,
    assessments: list[dict],
    **kwargs: Any,
) -> dict:
    """Aggregate crowd-sourced risk assessments into a confidence-weighted consensus.

    Workflow:
        1. Validate and clamp risk_score to [1, 10] and confidence to [0, 1].
        2. Compute confidence-weighted mean and standard deviation.
        3. Flag assessors whose score deviates > 2 stddev from the mean.
        4. Classify consensus strength based on stddev thresholds.

    Args:
        asset_id: Identifier for the asset being audited (e.g., ticker, contract).
        assessments: List of assessment dicts, each with:
            assessor_id (str): Unique assessor identifier.
            risk_score (float): Risk rating 1 (very low) to 10 (very high).
            confidence (float): Assessor self-reported confidence 0.0-1.0.
            rationale (str): Free-text explanation.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        Dict with keys:
            status (str): "success" or "error".
            asset_id (str): Echoed input.
            consensus_risk_score (float): Confidence-weighted mean score.
            consensus_level (str): "strong", "moderate", or "weak".
            weighted_stddev (float): Spread of scores, weighted by confidence.
            outlier_assessments (list[dict]): Assessors beyond 2 stddev.
            assessment_count (int): Total valid assessments received.
            risk_label (str): Human-readable label for the consensus score.
            timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        if not assessments:
            return {
                "status": "success",
                "asset_id": asset_id,
                "consensus_risk_score": 0.0,
                "consensus_level": "weak",
                "weighted_stddev": 0.0,
                "outlier_assessments": [],
                "assessment_count": 0,
                "risk_label": "insufficient_data",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Validate and normalize each assessment
        valid: list[dict] = []
        for a in assessments:
            try:
                score = float(a["risk_score"])
                confidence = float(a["confidence"])
                score = max(1.0, min(10.0, score))
                confidence = max(0.0, min(1.0, confidence))
                valid.append({
                    "assessor_id": a.get("assessor_id", "unknown"),
                    "risk_score": score,
                    "confidence": confidence,
                    "rationale": a.get("rationale", ""),
                })
            except (KeyError, ValueError, TypeError):
                continue  # skip malformed entries

        if not valid:
            return {
                "status": "success",
                "asset_id": asset_id,
                "consensus_risk_score": 0.0,
                "consensus_level": "weak",
                "weighted_stddev": 0.0,
                "outlier_assessments": [],
                "assessment_count": 0,
                "risk_label": "no_valid_assessments",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        scores = [a["risk_score"] for a in valid]
        weights = [max(a["confidence"], 0.01) for a in valid]  # floor at 0.01 to avoid zero-weight

        mean, stddev = _weighted_stats(scores, weights)

        # Detect outliers
        outlier_assessments: list[dict] = []
        if stddev > 0:
            for a, s, w in zip(valid, scores, weights):
                z = abs(s - mean) / stddev
                if z > OUTLIER_Z_THRESHOLD:
                    outlier_assessments.append({
                        **a,
                        "z_score": round(z, 4),
                        "deviation_from_mean": round(s - mean, 4),
                    })

        consensus_level = _classify_consensus(stddev)

        # Human-readable risk label based on mean
        if mean <= 2.5:
            risk_label = "very_low"
        elif mean <= 4.0:
            risk_label = "low"
        elif mean <= 6.0:
            risk_label = "moderate"
        elif mean <= 8.0:
            risk_label = "high"
        else:
            risk_label = "very_high"

        return {
            "status": "success",
            "asset_id": asset_id,
            "consensus_risk_score": mean,
            "consensus_level": consensus_level,
            "weighted_stddev": stddev,
            "outlier_assessments": outlier_assessments,
            "assessment_count": len(valid),
            "risk_label": risk_label,
            "score_range": {"min": min(scores), "max": max(scores)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"crowd_sourced_risk_audit failed: {e}")
        _log_lesson(f"crowd_sourced_risk_audit: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to logs/lessons.md.

    Args:
        message: Description of the error or lesson.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
