"""Compare DeFi protocols yielding opportunities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "defi_yield_comparator",
    "description": "Filters DeFi protocols by safety heuristics and ranks risk-adjusted yield.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "protocols": {"type": "array", "items": {"type": "object"}},
            "min_tvl": {"type": "number", "default": 1_000_000},
            "require_audit": {"type": "boolean", "default": True},
        },
        "required": ["protocols"],
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


def defi_yield_comparator(
    protocols: list[dict[str, Any]],
    min_tvl: float = 1_000_000,
    require_audit: bool = True,
    **_: Any,
) -> dict[str, Any]:
    """Return ranked list of DeFi opportunities."""
    try:
        ranked = []
        for protocol in protocols:
            tvl = float(protocol.get("tvl_usd", 0.0))
            audited = protocol.get("audit_status") == "audited"
            if tvl < min_tvl:
                continue
            if require_audit and not audited:
                continue
            apy = float(protocol.get("apy_pct", 0.0))
            tvl_score = min(tvl / (10 * min_tvl), 2.0)
            audit_bonus = 1.0 if audited else 0.7
            risk_adjusted = apy * tvl_score * audit_bonus
            ranked.append(
                {
                    "name": protocol.get("name"),
                    "chain": protocol.get("chain"),
                    "asset": protocol.get("asset"),
                    "apy_pct": apy,
                    "tvl_usd": tvl,
                    "audited": audited,
                    "risk_adjusted_yield": round(risk_adjusted, 2),
                }
            )
        ranked.sort(key=lambda item: item["risk_adjusted_yield"], reverse=True)
        data = {"protocols": ranked}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("defi_yield_comparator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
