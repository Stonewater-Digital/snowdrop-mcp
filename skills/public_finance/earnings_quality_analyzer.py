"""Assess earnings quality via accruals and Beneish metrics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "earnings_quality_analyzer",
    "description": "Computes accrual ratios, Beneish M-Score, and manipulation risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "financials": {"type": "object"},
        },
        "required": ["financials"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def earnings_quality_analyzer(financials: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return accrual metrics and Beneish M-score."""
    try:
        ni = financials.get("net_income", 0.0)
        ocf = financials.get("operating_cash_flow", 0.0)
        avg_assets = (financials.get("total_assets", 0.0) + financials.get("total_assets_prior", 0.0)) / 2 or 1
        accruals_ratio = (ni - ocf) / avg_assets
        dsri = (financials.get("receivables", 0.0) / financials.get("revenue", 1)) / ((financials.get("receivables_prior", financials.get("receivables", 1)) / financials.get("revenue_prior", 1)) or 1)
        gmi = (financials.get("revenue_prior", 1) - financials.get("cogs_prior", financials.get("revenue_prior", 1) * 0.6)) / (financials.get("revenue", 1) - financials.get("cogs", financials.get("revenue", 1) * 0.6))
        aqi = (1 - (financials.get("current_assets", 0.0) + financials.get("ppe", 0.0)) / financials.get("total_assets", 1)) / (1 - (financials.get("current_assets_prior", 0.0) + financials.get("ppe_prior", 0.0)) / financials.get("total_assets_prior", 1))
        sgi = financials.get("revenue", 1) / financials.get("revenue_prior", 1)
        depi = (financials.get("depreciation_prior", 1) / (financials.get("ppe_prior", 1))) / ((financials.get("depreciation", 1) / (financials.get("ppe", 1))) or 1)
        m_score = (
            -4.84
            + 0.92 * dsri
            + 0.528 * gmi
            + 0.404 * aqi
            + 0.892 * sgi
            + 0.115 * depi
        )
        manipulation_risk = "high" if m_score > -1.78 else "low"
        red_flags = []
        if accruals_ratio > 0.1:
            red_flags.append("High accruals vs assets")
        if manipulation_risk == "high":
            red_flags.append("Beneish score indicates risk")
        data = {
            "quality_score": round(1 - accruals_ratio, 3),
            "accruals_ratio": round(accruals_ratio, 3),
            "m_score": round(m_score, 3),
            "manipulation_risk": manipulation_risk,
            "red_flags": red_flags,
            "assessment": "Monitor" if red_flags else "Clean",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("earnings_quality_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
