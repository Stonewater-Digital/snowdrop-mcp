"""Track agent funnel conversions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "agent_funnel_analyzer",
    "description": "Calculates conversion rates across registration, activation, engagement, and upgrade.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "agents": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["agents"],
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


STAGES = ["registered", "activated", "engaged", "upgraded", "churned"]


def agent_funnel_analyzer(agents: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return funnel metrics and bottlenecks."""
    try:
        counts = {stage: 0 for stage in STAGES}
        total_time_to_activate = 0.0
        activations = 0
        for agent in agents:
            counts["registered"] += 1
            first_call = agent.get("first_call_date")
            total_calls = int(agent.get("total_calls", 0))
            upgraded_date = agent.get("upgraded_date")
            churned = bool(agent.get("churned"))
            if first_call:
                counts["activated"] += 1
                activations += 1
                registered_date = datetime.fromisoformat(agent.get("registered_date"))
                first_dt = datetime.fromisoformat(first_call)
                total_time_to_activate += max((first_dt - registered_date).days, 0)
            if total_calls >= 10:
                counts["engaged"] += 1
            if upgraded_date:
                counts["upgraded"] += 1
            if churned:
                counts["churned"] += 1

        conversion_rates = _calc_conversion_rates(counts)
        bottleneck = min(conversion_rates, key=conversion_rates.get, default="registered")
        avg_time = (total_time_to_activate / activations) if activations else 0.0
        funnel = [{"stage": stage, "count": counts[stage]} for stage in STAGES]
        data = {
            "funnel": funnel,
            "conversion_rates": conversion_rates,
            "bottleneck": bottleneck,
            "avg_time_to_activate_days": round(avg_time, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("agent_funnel_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _calc_conversion_rates(counts: dict[str, int]) -> dict[str, float]:
    rates = {}
    registered = counts.get("registered", 0)
    rates["activation"] = counts.get("activated", 0) / registered if registered else 0.0
    activated = counts.get("activated", 0)
    rates["engagement"] = counts.get("engaged", 0) / activated if activated else 0.0
    engaged = counts.get("engaged", 0)
    rates["upgrade"] = counts.get("upgraded", 0) / engaged if engaged else 0.0
    rates["retention"] = 1 - (counts.get("churned", 0) / registered if registered else 0.0)
    return {k: round(v, 4) for k, v in rates.items()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
