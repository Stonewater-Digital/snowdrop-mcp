"""Supply chain risk insurance model.
Quantifies dependency exposure and necessary contingent business interruption limit.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "supply_chain_risk_insurance_model",
    "description": "Scores suppliers and calculates contingent BI exposure.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "suppliers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "spend": {"type": "number"},
                        "recovery_time_weeks": {"type": "number"},
                        "single_source": {"type": "boolean"},
                    },
                    "required": ["name", "spend", "recovery_time_weeks", "single_source"],
                },
            }
        },
        "required": ["suppliers"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def supply_chain_risk_insurance_model(suppliers: Sequence[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return contingency exposure and supplier stress ranking."""
    try:
        total_spend = sum(sup.get("spend", 0.0) for sup in suppliers)
        ranked = []
        exposure = 0.0
        for sup in suppliers:
            dependency_factor = 1.5 if sup.get("single_source") else 1.0
            supplier_exposure = sup["spend"] * sup["recovery_time_weeks"] / 52 * dependency_factor
            exposure += supplier_exposure
            score = dependency_factor * sup["recovery_time_weeks"]
            ranked.append(
                {
                    "name": sup["name"],
                    "exposure": round(supplier_exposure, 2),
                    "risk_score": round(score, 2),
                }
            )
        ranked.sort(key=lambda row: row["risk_score"], reverse=True)
        data = {
            "contingent_bi_limit": round(exposure, 2),
            "supplier_ranking": ranked,
            "dependency_ratio_pct": round(exposure / total_spend * 100 if total_spend else 0.0, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("supply_chain_risk_insurance_model failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
