"""Shared analytics helpers for crypto RWA skill modules."""

from __future__ import annotations

from typing import Any

CATEGORY_FALLBACK_METRICS: dict[str, list[dict[str, float]]] = {
    "asset_verification": [
        {"suffix": "parity_gap", "onchain": 1.0, "offchain": 1.0, "tolerance": 0.02, "weight": 1.0},
        {"suffix": "documentation_latency", "onchain": 0.0, "offchain": 0.0, "tolerance": 4.0, "weight": 0.6},
    ],
    "security_heuristics": [
        {"suffix": "attack_surface", "onchain": 0.15, "offchain": 0.1, "tolerance": 0.05, "weight": 1.2},
        {"suffix": "monitoring_latency", "onchain": 3.0, "offchain": 2.0, "tolerance": 4.0, "weight": 0.5},
    ],
    "oracle_reconciliation": [
        {"suffix": "price_gap", "onchain": 100.0, "offchain": 100.25, "tolerance": 0.75, "weight": 1.0},
        {"suffix": "latency_gap", "onchain": 60.0, "offchain": 30.0, "tolerance": 90.0, "weight": 0.5},
    ],
    "token_compliance": [
        {"suffix": "policy_alignment", "onchain": 0.9, "offchain": 1.0, "tolerance": 0.15, "weight": 1.0},
        {"suffix": "kyc_refresh", "onchain": 35.0, "offchain": 30.0, "tolerance": 20.0, "weight": 0.7},
    ],
}

DATA_SOURCE_HINTS: dict[str, list[str]] = {
    "asset_verification": ["issuer_reports", "custodian_exports", "public_records"],
    "security_heuristics": ["bytecode_audit", "simulated_transactions", "public_rpc"],
    "oracle_reconciliation": ["fred", "world_bank", "exchange_apis"],
    "token_compliance": ["governance_docs", "aml_systems", "registry_exports"],
}


def analyze_payload(
    *,
    skill_name: str,
    description: str,
    payload: dict[str, Any],
    focus_tag: str,
    category_tag: str,
    context: dict[str, Any] | None,
) -> dict[str, Any]:
    """Normalize payload data, compute risk metrics, and build structured telemetry."""

    observations = _normalize_observations(payload.get("observations"), category_tag, focus_tag)
    metrics, alerts, composite_score = _score_observations(observations)
    severity = _derive_severity(composite_score, alerts)
    summary = _build_summary(description, focus_tag, severity, alerts)
    recommendations = _build_recommendations(severity, focus_tag, alerts)
    data_sources = _determine_data_sources(payload, category_tag)

    return {
        "skill": skill_name,
        "description": description,
        "category": category_tag,
        "focus": focus_tag,
        "summary": summary,
        "severity": severity,
        "composite_score": composite_score,
        "alerts": alerts,
        "metrics": metrics,
        "recommendations": recommendations,
        "data_sources": data_sources,
        "context": {
            "provided_observation_count": len(payload.get("observations", []) or []),
            "notes": payload.get("notes"),
            "extras": context or {},
        },
    }


def _determine_data_sources(payload: dict[str, Any], category_tag: str) -> list[str]:
    """Return declared data sources with category defaults as fallback."""

    declared = payload.get("data_sources")
    if isinstance(declared, list) and declared:
        return [str(item) for item in declared]
    return DATA_SOURCE_HINTS.get(category_tag, ["synthetic"])


def _normalize_observations(
    raw: Any,
    category_tag: str,
    focus_tag: str,
) -> list[dict[str, float]]:
    """Coerce caller-provided observations to a normalized structure with fallbacks."""

    normalized: list[dict[str, float]] = []
    if isinstance(raw, list):
        for idx, candidate in enumerate(raw):
            if not isinstance(candidate, dict):
                continue
            metric = str(candidate.get("metric") or f"{focus_tag}_metric_{idx + 1}")
            onchain = _to_float(candidate.get("onchain"), 0.0)
            offchain = _to_float(candidate.get("offchain"), 0.0)
            tolerance = max(_to_float(candidate.get("tolerance"), 0.01), 1e-6)
            weight = max(_to_float(candidate.get("weight"), 1.0), 0.1)
            normalized.append(
                {
                    "metric": metric,
                    "onchain": onchain,
                    "offchain": offchain,
                    "tolerance": tolerance,
                    "weight": weight,
                    "notes": candidate.get("notes"),
                }
            )
    if normalized:
        return normalized
    return _build_default_observations(category_tag, focus_tag)


def _build_default_observations(category_tag: str, focus_tag: str) -> list[dict[str, float]]:
    """Synthesize deterministic fallback data so skills run without paid feeds."""

    default_metrics = CATEGORY_FALLBACK_METRICS.get(
        category_tag, CATEGORY_FALLBACK_METRICS["asset_verification"]
    )
    observations: list[dict[str, float]] = []
    for fallback in default_metrics:
        metric_name = f"{focus_tag}_{fallback['suffix']}"
        observations.append(
            {
                "metric": metric_name,
                "onchain": fallback["onchain"],
                "offchain": fallback["offchain"],
                "tolerance": fallback["tolerance"],
                "weight": fallback["weight"],
                "notes": "synthetic_fallback",
            }
        )
    return observations


def _score_observations(
    observations: list[dict[str, float]],
) -> tuple[list[dict[str, float]], list[dict[str, float]], float]:
    """Score normalized observations and return metrics, alerts, and a composite score."""

    metrics: list[dict[str, float]] = []
    alerts: list[dict[str, float]] = []
    total_weight = 0.0
    weighted_sum = 0.0

    for observation in observations:
        onchain = observation["onchain"]
        offchain = observation["offchain"]
        tolerance = observation["tolerance"]
        weight = observation["weight"]

        delta = abs(onchain - offchain)
        ratio = delta / tolerance if tolerance else 0.0
        health = max(0.0, 1.2 - min(ratio, 2.0))

        metric_payload = {
            "metric": observation["metric"],
            "onchain": onchain,
            "offchain": offchain,
            "delta": round(delta, 6),
            "gap_ratio": round(ratio, 6),
            "tolerance": tolerance,
            "weight": weight,
            "health": round(health, 4),
            "notes": observation.get("notes"),  # type: ignore[arg-type]
        }
        metrics.append(metric_payload)

        total_weight += weight
        weighted_sum += health * weight

        if delta > tolerance:
            alerts.append(metric_payload)

    if total_weight == 0:
        return metrics, alerts, 1.0
    return metrics, alerts, round(weighted_sum / total_weight, 4)


def _derive_severity(composite_score: float, alerts: list[dict[str, float]]) -> str:
    """Map composite score plus alert count to a qualitative severity."""

    if composite_score < 0.55 or len(alerts) > 2:
        return "critical"
    if composite_score < 0.8 or alerts:
        return "attention"
    return "stable"


def _build_summary(
    description: str,
    focus_tag: str,
    severity: str,
    alerts: list[dict[str, float]],
) -> str:
    """Compose a friendly natural-language summary for MCP clients."""

    base = f"{description} Focus: {focus_tag.replace('_', ' ')}."
    if severity == "stable":
        tail = " Signals are within tolerance and synthetic controls match submitted data."
    elif severity == "attention":
        alert_hint = alerts[0]["metric"] if alerts else "noisy metric"
        tail = f" At least one metric (e.g., {alert_hint}) is brushing limits — plan remediation."
    else:
        alert_hint = alerts[0]["metric"] if alerts else "core metric"
        tail = f" Critical drift detected on {alert_hint}; route to Thunder before settlement."
    return base + tail


def _build_recommendations(
    severity: str,
    focus_tag: str,
    alerts: list[dict[str, float]],
) -> list[str]:
    """Provide deterministic action items for operators."""

    recs: list[str] = []
    readable_focus = focus_tag.replace("_", " ")
    if severity == "stable":
        recs.append(f"Keep passive monitoring active for {readable_focus} exposures.")
    elif severity == "attention":
        recs.append(f"Review supporting documents tied to {readable_focus} before next cycle.")
    else:
        recs.append(f"Escalate {readable_focus} package to thunder_signal within 30 minutes.")
    if alerts:
        recs.append(f"Drill into {alerts[0]['metric']} to reconcile gap ratio {alerts[0]['gap_ratio']}.")
    recs.append("Update Travel Rule / compliance packets once discrepancies close.")
    return recs


def _to_float(value: Any, fallback: float) -> float:
    """Convert any value to float with defensive fallback."""

    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


__all__ = ["analyze_payload"]
