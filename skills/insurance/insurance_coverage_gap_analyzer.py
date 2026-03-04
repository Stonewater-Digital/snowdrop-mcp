"""Analyze insurance coverage gaps across life, disability, and health categories.

MCP Tool Name: insurance_coverage_gap_analyzer
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "insurance_coverage_gap_analyzer",
    "description": "Analyze insurance coverage gaps across life, disability, and health categories. Provides per-category gap analysis and an overall protection score.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_assets": {"type": "number", "description": "Total assets / net worth."},
            "total_liabilities": {"type": "number", "description": "Total outstanding liabilities."},
            "current_life": {"type": "number", "description": "Current life insurance coverage."},
            "current_disability": {"type": "number", "description": "Current monthly disability benefit."},
            "current_health_oop_max": {"type": "number", "description": "Current health plan out-of-pocket maximum."},
            "dependents": {"type": "integer", "description": "Number of dependents (default 0).", "default": 0},
        },
        "required": [
            "total_assets", "total_liabilities",
            "current_life", "current_disability", "current_health_oop_max",
        ],
    },
}


def insurance_coverage_gap_analyzer(
    total_assets: float,
    total_liabilities: float,
    current_life: float,
    current_disability: float,
    current_health_oop_max: float,
    dependents: int = 0,
) -> dict[str, Any]:
    """Analyze insurance coverage gaps."""
    try:
        gaps = {}
        scores = []

        # Life insurance: should cover liabilities + 10x income proxy (assets/5 as rough income)
        estimated_income = total_assets / 5 if total_assets > 0 else 50000
        life_need = total_liabilities + (estimated_income * 10 * max(dependents, 1))
        life_gap = max(life_need - current_life, 0)
        life_score = min(current_life / life_need * 100, 100) if life_need > 0 else 100
        gaps["life"] = {
            "need": round(life_need, 2),
            "current": current_life,
            "gap": round(life_gap, 2),
            "score": round(life_score, 1),
        }
        scores.append(life_score)

        # Disability: should cover 60% of estimated monthly income
        monthly_income_est = estimated_income / 12
        disability_need = monthly_income_est * 0.60
        disability_gap = max(disability_need - current_disability, 0)
        disability_score = min(current_disability / disability_need * 100, 100) if disability_need > 0 else 100
        gaps["disability"] = {
            "monthly_need": round(disability_need, 2),
            "current_monthly": current_disability,
            "monthly_gap": round(disability_gap, 2),
            "score": round(disability_score, 1),
        }
        scores.append(disability_score)

        # Health: OOP max should be < 10% of liquid assets
        liquid_assets_est = total_assets * 0.20  # assume 20% liquid
        health_threshold = liquid_assets_est * 0.10
        health_adequate = current_health_oop_max <= health_threshold if health_threshold > 0 else True
        health_score = 100 if health_adequate else max(50 - (current_health_oop_max - health_threshold) / 100, 0)
        gaps["health"] = {
            "oop_max": current_health_oop_max,
            "recommended_max_oop": round(health_threshold, 2),
            "adequate": health_adequate,
            "score": round(health_score, 1),
        }
        scores.append(health_score)

        overall_score = sum(scores) / len(scores) if scores else 0

        return {
            "status": "ok",
            "data": {
                "total_assets": total_assets,
                "total_liabilities": total_liabilities,
                "dependents": dependents,
                "gaps": gaps,
                "overall_protection_score": round(overall_score, 1),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
