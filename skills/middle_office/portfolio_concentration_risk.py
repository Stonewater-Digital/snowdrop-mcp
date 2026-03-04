"""Portfolio concentration risk checker."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "portfolio_concentration_risk",
    "description": "Flags single-name, sector, and factor concentration breaches.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {"type": "array", "items": {"type": "object"}},
            "limits": {"type": "object"},
        },
        "required": ["positions", "limits"],
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


def portfolio_concentration_risk(
    positions: list[dict[str, Any]],
    limits: dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    """Return breaches, counts, and concentration score."""
    try:
        max_single = limits.get("max_single_name_pct", 1.0)
        max_sector = limits.get("max_sector_pct", 1.0)
        max_factor = limits.get("max_factor_exposure", 1.0)
        breaches: list[dict[str, Any]] = []
        sector_totals: dict[str, float] = {}
        factor_totals: dict[str, float] = {}
        for position in positions or []:
            weight_pct = float(position.get("weight_pct", 0.0))
            security_id = position.get("security_id", "unknown")
            sector = position.get("sector", "unknown")
            if weight_pct > max_single:
                breaches.append({"type": "single_name", "name": security_id, "value": weight_pct, "limit": max_single})
            sector_totals[sector] = sector_totals.get(sector, 0.0) + weight_pct
            for factor, exposure in (position.get("factor_exposures") or {}).items():
                factor_totals[factor] = factor_totals.get(factor, 0.0) + float(exposure)
        for sector, total in sector_totals.items():
            if total > max_sector:
                breaches.append({"type": "sector", "name": sector, "value": total, "limit": max_sector})
        for factor, total in factor_totals.items():
            if abs(total) > max_factor:
                breaches.append({"type": "factor", "name": factor, "value": total, "limit": max_factor})
        breach_count = len(breaches)
        concentration_score = max(0, 100 - breach_count * 10)
        status = "ok" if breach_count == 0 else "breach"
        data = {
            "breaches": breaches,
            "breach_count": breach_count,
            "concentration_score": concentration_score,
            "status": status,
        }
        return {"status": "ok", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        try:
            with open("logs/lessons.md", "a") as _f:
                _f.write(f"- [{datetime.now(timezone.utc).isoformat()}] portfolio_concentration_risk: {exc}\n")
        except OSError:
            pass
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
