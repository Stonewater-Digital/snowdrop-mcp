"""
Executive Summary: Monitors debt covenants by comparing current financial ratios to thresholds and calculating distance-to-breach percentages.

Inputs: covenants (list[dict]: name str, type str, threshold float, current_value float)
Outputs: dict with in_compliance (bool), breaches (list[str]), distances (list[dict]), summary (str)
MCP Tool Name: debt_covenant_monitor
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "debt_covenant_monitor",
    "description": (
        "Evaluates debt covenants against current financial ratios. "
        "Supports leverage_ratio (lower is better), interest_coverage (higher is better), "
        "and current_ratio (higher is better) covenant types. "
        "Returns breach status and distance-to-breach for each covenant."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "covenants": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Covenant identifier, e.g. 'Senior Leverage Ratio'"},
                        "type": {
                            "type": "string",
                            "enum": ["leverage_ratio", "interest_coverage", "current_ratio"],
                            "description": "Covenant type determines compliance direction"
                        },
                        "threshold": {"type": "number", "description": "Contractual limit/floor"},
                        "current_value": {"type": "number", "description": "Current measured ratio"}
                    },
                    "required": ["name", "type", "threshold", "current_value"]
                },
                "description": "List of debt covenants to evaluate"
            }
        },
        "required": ["covenants"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "in_compliance": {"type": "boolean"},
            "breaches": {"type": "array", "items": {"type": "string"}},
            "distances": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "distance_pct": {"type": "number"},
                        "current_value": {"type": "number"},
                        "threshold": {"type": "number"},
                        "status": {"type": "string"}
                    }
                }
            },
            "summary": {"type": "string"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["in_compliance", "breaches", "distances", "summary", "status", "timestamp"]
    }
}

# Covenant types where current_value must stay BELOW threshold (e.g. debt/EBITDA <= 4.0x)
_UPPER_BOUND_TYPES = {"leverage_ratio"}
# Covenant types where current_value must stay ABOVE threshold (e.g. interest coverage >= 2.0x)
_LOWER_BOUND_TYPES = {"interest_coverage", "current_ratio"}


def _check_compliance(covenant_type: str, threshold: float, current_value: float) -> bool:
    """Determine if a single covenant is in compliance.

    Args:
        covenant_type: One of 'leverage_ratio', 'interest_coverage', 'current_ratio'.
        threshold: The contractual limit.
        current_value: The measured ratio.

    Returns:
        True if compliant, False if breached.
    """
    if covenant_type in _UPPER_BOUND_TYPES:
        return current_value <= threshold
    elif covenant_type in _LOWER_BOUND_TYPES:
        return current_value >= threshold
    else:
        # Default: treat as upper bound
        return current_value <= threshold


def _distance_to_breach(covenant_type: str, threshold: float, current_value: float) -> float:
    """Calculate how far the current value is from breaching the covenant.

    A positive percentage means headroom remains (safe).
    A negative percentage means the covenant is already breached.

    For upper-bound covenants (leverage): distance = (threshold - current) / threshold * 100
    For lower-bound covenants (coverage): distance = (current - threshold) / threshold * 100

    Args:
        covenant_type: One of 'leverage_ratio', 'interest_coverage', 'current_ratio'.
        threshold: The contractual limit.
        current_value: The measured ratio.

    Returns:
        Distance-to-breach as a percentage (positive = headroom, negative = breached).

    Raises:
        ZeroDivisionError: If threshold is zero.
    """
    if threshold == 0:
        raise ZeroDivisionError(f"Covenant threshold is zero — cannot compute distance for covenant type '{covenant_type}'")

    if covenant_type in _UPPER_BOUND_TYPES:
        return round((threshold - current_value) / threshold * 100, 4)
    else:
        return round((current_value - threshold) / threshold * 100, 4)


def debt_covenant_monitor(**kwargs: Any) -> dict:
    """Monitor debt covenants and report compliance status with distance-to-breach metrics.

    Evaluates each covenant based on its type:
    - leverage_ratio: current_value must be <= threshold (lower is better)
    - interest_coverage: current_value must be >= threshold (higher is better)
    - current_ratio: current_value must be >= threshold (higher is better)

    Args:
        **kwargs: Keyword arguments containing:
            covenants (list[dict]): Each dict must have:
                - name (str): Covenant display name
                - type (str): 'leverage_ratio' | 'interest_coverage' | 'current_ratio'
                - threshold (float): Contractual limit
                - current_value (float): Current measured ratio

    Returns:
        dict: Contains:
            - status (str): 'success' or 'error'
            - in_compliance (bool): True only if ALL covenants pass
            - breaches (list[str]): Names of breached covenants
            - distances (list[dict]): Per-covenant distance-to-breach detail
            - summary (str): Human-readable compliance summary
            - timestamp (str): ISO 8601 UTC timestamp
    """
    try:
        covenants: list[dict] = kwargs.get("covenants", [])

        if not covenants:
            raise ValueError("No covenants provided — 'covenants' list is empty or missing")

        breaches: list[str] = []
        distances: list[dict] = []

        for cov in covenants:
            name: str = cov["name"]
            cov_type: str = cov["type"]
            threshold: float = float(cov["threshold"])
            current_value: float = float(cov["current_value"])

            if cov_type not in (_UPPER_BOUND_TYPES | _LOWER_BOUND_TYPES):
                raise ValueError(
                    f"Unknown covenant type '{cov_type}' for '{name}'. "
                    f"Expected one of: leverage_ratio, interest_coverage, current_ratio"
                )

            compliant = _check_compliance(cov_type, threshold, current_value)
            dist_pct = _distance_to_breach(cov_type, threshold, current_value)

            if not compliant:
                breaches.append(name)

            distances.append({
                "name": name,
                "type": cov_type,
                "current_value": current_value,
                "threshold": threshold,
                "distance_pct": dist_pct,
                "status": "COMPLIANT" if compliant else "BREACHED",
                "headroom": max(0.0, dist_pct),
            })

        in_compliance = len(breaches) == 0
        total = len(covenants)
        passed = total - len(breaches)

        if in_compliance:
            # Find the tightest covenant (smallest positive distance)
            min_headroom = min(d["distance_pct"] for d in distances)
            summary = (
                f"All {total} covenants in compliance. "
                f"Tightest headroom: {min_headroom:.2f}%."
            )
        else:
            breach_detail = ", ".join(
                f"{d['name']} ({d['distance_pct']:.2f}%)"
                for d in distances if d["status"] == "BREACHED"
            )
            summary = (
                f"COVENANT BREACH: {len(breaches)} of {total} covenants violated. "
                f"{passed} passing. Breached: {breach_detail}."
            )

        result = {
            "in_compliance": in_compliance,
            "breaches": breaches,
            "distances": distances,
            "summary": summary,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"debt_covenant_monitor failed: {e}")
        _log_lesson(f"debt_covenant_monitor: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the shared lessons log.

    Args:
        message: The lesson or error description to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
