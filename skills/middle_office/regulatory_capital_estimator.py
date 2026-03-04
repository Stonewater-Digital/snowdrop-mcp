"""Estimate regulatory capital requirements."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "regulatory_capital_estimator",
    "description": "Estimates Basel-style RWA and capital ratios for market risk books.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {"type": "array", "items": {"type": "object"}},
            "tier1_capital": {"type": "number"},
        },
        "required": ["positions", "tier1_capital"],
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


def regulatory_capital_estimator(positions: list[dict[str, Any]], tier1_capital: float, **_: Any) -> dict[str, Any]:
    """Return RWA, required capital, and adequacy ratio."""
    try:
        rwa_breakdown: list[dict[str, Any]] = []
        total_rwa = 0.0
        for position in positions or []:
            notional = float(position.get("notional", 0.0))
            risk_weight_pct = float(position.get("risk_weight_pct", 0.0))
            asset_class = position.get("asset_class", "other")
            rwa = notional * risk_weight_pct / 100.0
            total_rwa += rwa
            rwa_breakdown.append(
                {
                    "asset_class": asset_class,
                    "notional": notional,
                    "risk_weight_pct": risk_weight_pct,
                    "rwa": round(rwa, 2),
                }
            )
        capital_requirement = total_rwa * 0.08
        ratio = tier1_capital / total_rwa if total_rwa else 0.0
        buffer_to_minimum = ratio - 0.08
        data = {
            "total_rwa": round(total_rwa, 2),
            "capital_requirement": round(capital_requirement, 2),
            "capital_adequacy_ratio_pct": round(ratio * 100, 2),
            "buffer_to_minimum_pct": round(buffer_to_minimum * 100, 2),
            "position_rwa_breakdown": rwa_breakdown,
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] regulatory_capital_estimator: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
