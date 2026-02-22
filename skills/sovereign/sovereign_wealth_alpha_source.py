"""
Executive Summary: Screens nation-state investment opportunities against sovereign fund criteria (return, risk, ESG, sector, region), ranks by return/risk ratio, and identifies the top pick.
Inputs: criteria (dict: min_return_pct, max_risk_score, sectors, regions, esg_minimum), opportunities (list[dict]: name, country, sector, expected_return, risk_score, esg_score, min_investment)
Outputs: qualifying (list sorted by score), filtered_count (int), top_pick (dict), sector_distribution (dict)
MCP Tool Name: sovereign_wealth_alpha_source
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone
from collections import defaultdict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "sovereign_wealth_alpha_source",
    "description": "Screens and ranks sovereign wealth fund investment opportunities by return/risk ratio against configurable criteria.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "criteria": {
                "type": "object",
                "description": "Investment screening criteria",
                "properties": {
                    "min_return_pct": {"type": "number", "description": "Minimum expected annual return (%)"},
                    "max_risk_score": {"type": "number", "description": "Maximum allowed risk score (0-10 scale, 10 = highest risk)"},
                    "sectors": {"type": "array", "items": {"type": "string"}, "description": "Allowed sectors (empty = all)"},
                    "regions": {"type": "array", "items": {"type": "string"}, "description": "Allowed regions/countries (empty = all)"},
                    "esg_minimum": {"type": "number", "description": "Minimum ESG score (0-100 scale)"},
                    "max_min_investment": {"type": "number", "description": "Maximum acceptable minimum investment in USD (optional)"}
                },
                "required": ["min_return_pct", "max_risk_score", "esg_minimum"]
            },
            "opportunities": {
                "type": "array",
                "description": "Investment opportunities to evaluate",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "country": {"type": "string"},
                        "sector": {"type": "string"},
                        "expected_return": {"type": "number", "description": "Expected annual return (%)"},
                        "risk_score": {"type": "number", "description": "Risk score 0-10"},
                        "esg_score": {"type": "number", "description": "ESG score 0-100"},
                        "min_investment": {"type": "number", "description": "Minimum investment in USD"}
                    },
                    "required": ["name", "country", "sector", "expected_return", "risk_score", "esg_score", "min_investment"]
                }
            }
        },
        "required": ["criteria", "opportunities"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "qualifying": {"type": "array"},
                    "filtered_count": {"type": "integer"},
                    "top_pick": {"type": "object"},
                    "sector_distribution": {"type": "object"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}


def _compute_alpha_score(
    expected_return: float,
    risk_score: float,
    esg_score: float,
    return_weight: float = 0.50,
    risk_weight: float = 0.35,
    esg_weight: float = 0.15,
) -> float:
    """Compute a composite alpha score for ranking investment opportunities.

    Score = (return_normalized * return_weight)
           + (risk_inverted_normalized * risk_weight)
           + (esg_normalized * esg_weight)

    Normalization assumptions:
      - Return: 0-30% range normalized to 0-1
      - Risk: 0-10 inverted (lower risk = higher score), normalized to 0-1
      - ESG: 0-100 normalized to 0-1

    Args:
        expected_return: Expected annual return in percent.
        risk_score: Risk score on 0-10 scale (10 = highest risk).
        esg_score: ESG score on 0-100 scale (100 = best).
        return_weight: Weight for return component (default: 0.50).
        risk_weight: Weight for risk component (default: 0.35).
        esg_weight: Weight for ESG component (default: 0.15).

    Returns:
        float: Composite alpha score (0.0–1.0 scale).
    """
    return_norm = min(expected_return / 30.0, 1.0)          # Cap at 30% return
    risk_norm = max(0.0, (10.0 - risk_score) / 10.0)        # Invert: lower risk = higher score
    esg_norm = min(esg_score / 100.0, 1.0)

    score = (
        return_norm * return_weight
        + risk_norm * risk_weight
        + esg_norm * esg_weight
    )
    return round(score, 6)


def _passes_criteria(
    opp: dict[str, Any],
    criteria: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Check whether an opportunity passes all screening criteria.

    Args:
        opp: Opportunity dict with expected_return, risk_score, esg_score,
            sector, country, min_investment.
        criteria: Criteria dict with min_return_pct, max_risk_score,
            esg_minimum, sectors (list), regions (list), max_min_investment.

    Returns:
        tuple[bool, list[str]]: (passes, list of failure reasons).
    """
    failures: list[str] = []

    expected_return = float(opp.get("expected_return", 0))
    risk_score = float(opp.get("risk_score", 10))
    esg_score = float(opp.get("esg_score", 0))
    sector = str(opp.get("sector", "")).lower().strip()
    country = str(opp.get("country", "")).lower().strip()
    min_investment = float(opp.get("min_investment", 0))

    min_return = float(criteria.get("min_return_pct", 0))
    max_risk = float(criteria.get("max_risk_score", 10))
    esg_min = float(criteria.get("esg_minimum", 0))
    allowed_sectors = [s.lower().strip() for s in criteria.get("sectors", [])]
    allowed_regions = [r.lower().strip() for r in criteria.get("regions", [])]
    max_min_inv = criteria.get("max_min_investment")

    if expected_return < min_return:
        failures.append(f"return {expected_return}% < min {min_return}%")
    if risk_score > max_risk:
        failures.append(f"risk {risk_score} > max {max_risk}")
    if esg_score < esg_min:
        failures.append(f"ESG {esg_score} < min {esg_min}")
    if allowed_sectors and sector not in allowed_sectors:
        failures.append(f"sector '{sector}' not in allowed sectors")
    if allowed_regions and country not in allowed_regions:
        failures.append(f"country '{country}' not in allowed regions")
    if max_min_inv is not None and min_investment > float(max_min_inv):
        failures.append(f"min_investment ${min_investment:,.0f} > max ${float(max_min_inv):,.0f}")

    return len(failures) == 0, failures


def sovereign_wealth_alpha_source(
    criteria: dict[str, Any],
    opportunities: list[dict[str, Any]],
    **kwargs: Any
) -> dict[str, Any]:
    """Screen and rank sovereign investment opportunities by alpha score.

    Applies multi-factor filtering (return, risk, ESG, sector, region,
    min investment) then ranks survivors by composite alpha score
    (return/risk/ESG weighted). Produces sector distribution analysis.

    Args:
        criteria: Screening thresholds. Required keys:
            - min_return_pct (float): Minimum expected annual return %.
            - max_risk_score (float): Maximum allowed risk score (0-10).
            - esg_minimum (float): Minimum ESG score (0-100).
            Optional keys: 'sectors' (list[str]), 'regions' (list[str]),
            'max_min_investment' (float).
        opportunities: List of investment opportunity dicts. Each must have:
            'name', 'country', 'sector', 'expected_return', 'risk_score',
            'esg_score', 'min_investment'.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): Results including qualifying (list sorted by
              alpha_score descending), filtered_count (int of rejected),
              top_pick (dict), sector_distribution (dict), avg_return (float),
              avg_risk (float), avg_esg (float), screening_summary.
            - timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        if not opportunities:
            raise ValueError("opportunities list must be non-empty")

        qualifying: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []

        for opp in opportunities:
            name = str(opp.get("name", "UNNAMED")).strip()
            country = str(opp.get("country", "")).strip()
            sector = str(opp.get("sector", "")).strip()
            expected_return = float(opp.get("expected_return", 0))
            risk_score = float(opp.get("risk_score", 10))
            esg_score = float(opp.get("esg_score", 0))
            min_investment = float(opp.get("min_investment", 0))

            passes, failure_reasons = _passes_criteria(opp, criteria)
            alpha_score = _compute_alpha_score(expected_return, risk_score, esg_score)
            return_risk_ratio = round(expected_return / max(risk_score, 0.1), 4)

            record = {
                "name": name,
                "country": country,
                "sector": sector,
                "expected_return_pct": expected_return,
                "risk_score": risk_score,
                "esg_score": esg_score,
                "min_investment_usd": min_investment,
                "alpha_score": alpha_score,
                "return_risk_ratio": return_risk_ratio,
            }

            if passes:
                qualifying.append(record)
            else:
                rejected.append({**record, "rejection_reasons": failure_reasons})

        # Sort qualifying by alpha_score descending
        qualifying = sorted(qualifying, key=lambda x: x["alpha_score"], reverse=True)

        # Add rank
        for i, q in enumerate(qualifying, 1):
            q["rank"] = i

        top_pick: dict[str, Any] = qualifying[0] if qualifying else {}

        # Sector distribution across qualifying
        sector_counts: dict[str, int] = defaultdict(int)
        sector_return_sum: dict[str, float] = defaultdict(float)
        sector_risk_sum: dict[str, float] = defaultdict(float)

        for q in qualifying:
            s = q["sector"]
            sector_counts[s] += 1
            sector_return_sum[s] += q["expected_return_pct"]
            sector_risk_sum[s] += q["risk_score"]

        sector_distribution: dict[str, Any] = {}
        for s, count in sector_counts.items():
            sector_distribution[s] = {
                "count": count,
                "pct_of_qualifying": round(count / len(qualifying) * 100, 2) if qualifying else 0.0,
                "avg_return_pct": round(sector_return_sum[s] / count, 4),
                "avg_risk_score": round(sector_risk_sum[s] / count, 4),
            }

        # Summary stats for qualifying set
        avg_return = (
            round(sum(q["expected_return_pct"] for q in qualifying) / len(qualifying), 4)
            if qualifying else 0.0
        )
        avg_risk = (
            round(sum(q["risk_score"] for q in qualifying) / len(qualifying), 4)
            if qualifying else 0.0
        )
        avg_esg = (
            round(sum(q["esg_score"] for q in qualifying) / len(qualifying), 4)
            if qualifying else 0.0
        )
        avg_alpha = (
            round(sum(q["alpha_score"] for q in qualifying) / len(qualifying), 6)
            if qualifying else 0.0
        )

        screening_summary: dict[str, Any] = {
            "total_evaluated": len(opportunities),
            "qualifying_count": len(qualifying),
            "filtered_count": len(rejected),
            "pass_rate_pct": round(len(qualifying) / len(opportunities) * 100, 2) if opportunities else 0.0,
            "criteria_applied": {
                "min_return_pct": criteria.get("min_return_pct"),
                "max_risk_score": criteria.get("max_risk_score"),
                "esg_minimum": criteria.get("esg_minimum"),
                "sectors_filter": criteria.get("sectors", []),
                "regions_filter": criteria.get("regions", []),
                "max_min_investment": criteria.get("max_min_investment"),
            },
            "top_rejection_reasons": _summarize_rejection_reasons(rejected),
        }

        result: dict[str, Any] = {
            "qualifying": qualifying,
            "filtered_count": len(rejected),
            "rejected_opportunities": rejected,
            "top_pick": top_pick,
            "sector_distribution": sector_distribution,
            "avg_return_pct": avg_return,
            "avg_risk_score": avg_risk,
            "avg_esg_score": avg_esg,
            "avg_alpha_score": avg_alpha,
            "screening_summary": screening_summary,
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"sovereign_wealth_alpha_source failed: {e}")
        _log_lesson(f"sovereign_wealth_alpha_source: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _summarize_rejection_reasons(rejected: list[dict[str, Any]]) -> dict[str, int]:
    """Summarize the most common rejection reason types.

    Args:
        rejected: List of rejected opportunity dicts, each with 'rejection_reasons'.

    Returns:
        dict: Mapping of reason prefix to count.
    """
    reason_counts: dict[str, int] = defaultdict(int)
    for r in rejected:
        for reason in r.get("rejection_reasons", []):
            # Extract the leading keyword (e.g. "return", "risk", "ESG")
            keyword = reason.split()[0]
            reason_counts[keyword] += 1
    return dict(sorted(reason_counts.items(), key=lambda x: x[1], reverse=True))


def _log_lesson(message: str) -> None:
    """Append a lesson/error entry to the shared lessons log.

    Args:
        message: Human-readable error or lesson description to append.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except Exception as log_err:
        logger.warning(f"_log_lesson write failed: {log_err}")
