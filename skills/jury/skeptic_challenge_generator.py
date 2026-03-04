"""Generate Grok-style contrarian challenges for a thesis."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skeptic_challenge_generator",
    "description": "Produces a structured counter-position with risks and precedents for a thesis.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "thesis": {"type": "string"},
            "supporting_evidence": {
                "type": "array",
                "items": {"type": "string"},
            },
            "asset_class": {"type": "string"},
        },
        "required": ["thesis", "supporting_evidence", "asset_class"],
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


def skeptic_challenge_generator(
    thesis: str,
    supporting_evidence: list[str],
    asset_class: str,
    **_: Any,
) -> dict[str, Any]:
    """Assemble a Grok-grade challenge for the provided thesis."""
    try:
        if not thesis.strip():
            raise ValueError("thesis cannot be empty")
        if not supporting_evidence:
            raise ValueError("supporting_evidence is required")

        normalized_asset = asset_class.lower()
        risk_factors = _derive_risk_factors(normalized_asset, supporting_evidence)
        precedents = _map_precedents(normalized_asset)
        counter_thesis = _build_counter_thesis(thesis, normalized_asset)
        worst_case_scenario = _build_worst_case(normalized_asset, risk_factors)

        data = {
            "counter_thesis": counter_thesis,
            "risk_factors": risk_factors,
            "historical_precedents": precedents,
            "worst_case_scenario": worst_case_scenario,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("skeptic_challenge_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _derive_risk_factors(asset_class: str, evidence: list[str]) -> list[str]:
    thematic = {
        "equity": ["multiple compression", "funding drought", "governance drift"],
        "crypto": ["protocol exploit", "liquidity rug", "regulatory delisting"],
        "fixed_income": ["duration mismatch", "counterparty downgrade", "inflation shock"],
        "real_estate": ["cap rate expansion", "tenant churn", "refi risk"],
    }
    risks = list(thematic.get(asset_class, ["execution slippage", "model overfitting", "macro shock"]))
    if len(evidence) < 2:
        risks.append("thin evidence stack")
    return risks[:5]


def _map_precedents(asset_class: str) -> list[str]:
    library = {
        "crypto": [
            "Terra collapse (2022)",
            "FTX balance-sheet opacity (2022)",
            "DAO hack governance reset (2016)",
        ],
        "equity": [
            "Softbank Vision Fund markdown cycle (2019)",
            "WeWork failed IPO (2019)",
        ],
        "fixed_income": ["SVB duration gap (2023)", "Long-Term Capital Management (1998)"],
    }
    return library.get(asset_class, ["Dot-com drawdown (2000)", "GFC contagion (2008)"])


def _build_counter_thesis(thesis: str, asset_class: str) -> str:
    return (
        f"Even if {thesis.strip()}, {asset_class} risk premia look mispriced; upside relies on"
        " consensus narratives remaining intact despite accumulating fragility."
    )


def _build_worst_case(asset_class: str, risks: list[str]) -> dict[str, Any]:
    severity = 0.35 if asset_class == "fixed_income" else 0.5
    return {
        "drawdown_pct": round(severity * 100, 2),
        "liquidity_shock_days": 7 if asset_class == "crypto" else 30,
        "narrative": f"Concurrent realization of {', '.join(risks[:3])} triggers cascading exits.",
        "contingency_plan": "Throttle deployment, rotate to cash, and re-run diligence with Grok-in-loop.",
    }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
