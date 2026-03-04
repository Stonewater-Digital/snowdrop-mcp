"""Compare health insurance plans by total estimated annual cost.

MCP Tool Name: health_insurance_plan_comparator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "health_insurance_plan_comparator",
    "description": "Compare health insurance plans by estimated total annual cost (premiums + out-of-pocket up to max) given expected medical costs. Ranks plans from cheapest to most expensive.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "plans": {
                "type": "array",
                "description": "List of health insurance plans.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Plan name."},
                        "premium": {"type": "number", "description": "Monthly premium."},
                        "deductible": {"type": "number", "description": "Annual deductible."},
                        "copay": {"type": "number", "description": "Per-visit copay."},
                        "oop_max": {"type": "number", "description": "Annual out-of-pocket maximum."},
                    },
                    "required": ["name", "premium", "deductible", "copay", "oop_max"],
                },
            },
            "expected_costs": {
                "type": "number",
                "description": "Expected annual medical costs before insurance.",
            },
        },
        "required": ["plans", "expected_costs"],
    },
}


def health_insurance_plan_comparator(
    plans: list[dict[str, Any]], expected_costs: float
) -> dict[str, Any]:
    """Compare health insurance plans by total estimated cost."""
    try:
        if not plans:
            return {
                "status": "error",
                "data": {"error": "plans list must not be empty."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        results = []
        for plan in plans:
            annual_premium = plan["premium"] * 12

            # Simplified OOP estimate: costs up to deductible are 100% OOP,
            # then coinsurance kicks in, capped at OOP max
            if expected_costs <= plan["deductible"]:
                oop = expected_costs
            else:
                # After deductible, assume 20% coinsurance on remainder
                post_deductible = expected_costs - plan["deductible"]
                coinsurance_cost = post_deductible * 0.20
                oop = min(plan["deductible"] + coinsurance_cost, plan["oop_max"])

            total = annual_premium + oop

            results.append({
                "name": plan["name"],
                "annual_premium": round(annual_premium, 2),
                "deductible": plan["deductible"],
                "oop_max": plan["oop_max"],
                "estimated_oop": round(oop, 2),
                "total_estimated_cost": round(total, 2),
            })

        results.sort(key=lambda x: x["total_estimated_cost"])
        for rank, item in enumerate(results, 1):
            item["rank"] = rank

        return {
            "status": "ok",
            "data": {
                "expected_medical_costs": expected_costs,
                "comparisons": results,
                "best_plan": results[0]["name"] if results else None,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
